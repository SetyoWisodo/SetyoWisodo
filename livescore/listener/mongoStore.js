'use strict';

// Store MongoDB untuk listener, memakai model yang sama dengan API (models/).
// Listener hanya membutuhkan find, insert, dan update pada koleksi soccer_*.

const SoccerLeague = require('../models/soccerLeague');
const SoccerClub = require('../models/soccerClub');
const SoccerMatch = require('../models/soccerMatch');
const SoccerMatchEvent = require('../models/soccerMatchEvent');
const SoccerStanding = require('../models/soccerStanding');
const SoccerSyncState = require('../models/soccerSyncState');

const DUPLICATE_KEY = 11000;

function createMongoStore() {
  return {
    async upsertLeague(slug, doc) {
      await SoccerLeague.updateOne({ slug }, { $set: doc }, { upsert: true });
    },

    async getLeague(slug) {
      return SoccerLeague.findOne({ slug }, { season: 1 }).lean();
    },

    async upsertClub(slug, doc) {
      const { source, ...rest } = doc;
      await SoccerClub.updateOne(
        { 'source.provider': source.provider, 'source.club_id': source.club_id },
        { $set: { ...rest, source }, $addToSet: { league_slugs: slug } },
        { upsert: true }
      );
    },

    async upsertMatch(slug, doc) {
      await SoccerMatch.updateOne(
        { 'source.provider': doc.source.provider, league_slug: slug, 'source.event_id': doc.source.event_id },
        { $set: doc },
        { upsert: true }
      );
    },

    async upsertStanding(slug, seasonYear, groupId, doc) {
      await SoccerStanding.updateOne(
        { league_slug: slug, season_year: seasonYear, group_id: groupId },
        { $set: doc },
        { upsert: true }
      );
    },

    async upsertEvents(docs) {
      if (docs.length === 0) return;
      await SoccerMatchEvent.bulkWrite(
        docs.map((doc) => ({
          updateOne: {
            filter: {
              'source.provider': doc.source.provider,
              league_slug: doc.league_slug,
              event_id: doc.event_id,
              'source.event_key': doc.source.event_key,
            },
            update: { $set: doc },
            upsert: true,
          },
        })),
        { ordered: false }
      );
    },

    async setPlayByPlayAvailable(slug, eventId, value) {
      await SoccerMatch.updateOne(
        { league_slug: slug, 'source.event_id': eventId },
        { $set: { play_by_play_available: value } }
      );
    },

    /** Pertandingan dalam rentang tanggal (YYYYMMDD) yang sedang atau sudah berlangsung. */
    async findMatchesForDetails(slug, fromYmd, toYmd) {
      const rows = await SoccerMatch.find(
        {
          league_slug: slug,
          scoreboard_date: { $gte: fromYmd, $lte: toYmd },
          'status.state': { $in: ['in', 'post'] },
        },
        { 'source.event_id': 1, 'status.state': 1, 'status.completed': 1 }
      ).lean();
      return rows.map((r) => ({
        event_id: r.source.event_id,
        state: r.status.state,
        completed: Boolean(r.status.completed),
      }));
    },

    async syncedPlayKeys(slug) {
      const rows = await SoccerSyncState.find(
        { provider: 'football-data', league_slug: slug, resource_type: 'plays', last_success_at: { $ne: null } },
        { resource_key: 1 }
      ).lean();
      return new Set(rows.map((r) => r.resource_key));
    },

    /**
     * Lease atomik. Mengembalikan false jika lease masih dipegang proses lain.
     * Jika dokumen sudah ada dan lease kedaluwarsa, lease diambil alih.
     */
    async acquireLease(key, owner, ttlMs, nowDate) {
      const expired = { $or: [{ 'lease.expires_at': { $lte: nowDate } }, { 'lease.owner': owner }, { 'lease.owner': '' }, { 'lease.owner': { $exists: false } }, { lease: { $exists: false } }] };
      try {
        const res = await SoccerSyncState.updateOne(
          { ...key, ...expired },
          {
            $set: {
              ...key,
              status: 'polling',
              lease: { owner, expires_at: new Date(nowDate.getTime() + ttlMs) },
            },
          },
          { upsert: true }
        );
        return res.upsertedCount + res.modifiedCount > 0;
      } catch (err) {
        if (err.code === DUPLICATE_KEY) return false;
        throw err;
      }
    },

    async releaseLease(key) {
      await SoccerSyncState.updateOne(key, { $set: { 'lease.owner': '', 'lease.expires_at': new Date(0) } });
    },

    async recordSync(key, set, inc = {}) {
      const update = { $set: { ...key, ...set } };
      if (Object.keys(inc).length) update.$inc = inc;
      await SoccerSyncState.updateOne(key, update, { upsert: true });
    },
  };
}

module.exports = { createMongoStore };
