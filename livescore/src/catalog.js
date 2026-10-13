// Katalog liga untuk provider mock (data simulasi).
// Nama tim adalah nama klub/tim nasional nyata, tetapi jadwal dan skor
// pada mode mock dibuat secara simulasi dan BUKAN hasil pertandingan sungguhan.
//
// slots = jam kick-off dalam UTC (desimal) per wilayah, supaya jadwal
// terasa realistis (Eropa malam waktu setempat, Asia sore, Amerika malam).

const SLOTS = {
  eu: [11.5, 14, 16.5, 19, 21],
  asia: [8, 10.5, 12.5, 13.5],
  am: [17, 19, 21, 23.5],
  intl: [13, 16, 19],
};

const RAW = [
  { id: 'epl', name: 'Premier League', country: 'Inggris', cc: 'GB', region: 'eu', teams: [
    ['Arsenal', 'ARS'], ['Chelsea', 'CHE'], ['Liverpool', 'LIV'], ['Manchester City', 'MCI'], ['Manchester United', 'MUN'], ['Tottenham', 'TOT'] ] },
  { id: 'laliga', name: 'La Liga', country: 'Spanyol', cc: 'ES', region: 'eu', teams: [
    ['Barcelona', 'BAR'], ['Real Madrid', 'RMA'], ['Atlético Madrid', 'ATM'], ['Sevilla', 'SEV'], ['Real Sociedad', 'RSO'], ['Villarreal', 'VIL'] ] },
  { id: 'seriea', name: 'Serie A', country: 'Italia', cc: 'IT', region: 'eu', teams: [
    ['Inter', 'INT'], ['AC Milan', 'MIL'], ['Juventus', 'JUV'], ['Napoli', 'NAP'], ['AS Roma', 'ROM'], ['Lazio', 'LAZ'] ] },
  { id: 'bundesliga', name: 'Bundesliga', country: 'Jerman', cc: 'DE', region: 'eu', teams: [
    ['Bayern München', 'FCB'], ['Borussia Dortmund', 'BVB'], ['RB Leipzig', 'RBL'], ['Bayer Leverkusen', 'B04'], ['Eintracht Frankfurt', 'SGE'], ['VfB Stuttgart', 'VFB'] ] },
  { id: 'ligue1', name: 'Ligue 1', country: 'Prancis', cc: 'FR', region: 'eu', teams: [
    ['Paris Saint-Germain', 'PSG'], ['Marseille', 'OM'], ['Lyon', 'OL'], ['Monaco', 'ASM'], ['Lille', 'LIL'], ['Nice', 'NIC'] ] },
  { id: 'eredivisie', name: 'Eredivisie', country: 'Belanda', cc: 'NL', region: 'eu', teams: [
    ['Ajax', 'AJX'], ['PSV Eindhoven', 'PSV'], ['Feyenoord', 'FEY'], ['AZ Alkmaar', 'AZ'], ['FC Twente', 'TWE'], ['FC Utrecht', 'UTR'] ] },
  { id: 'liga1id', name: 'BRI Liga 1', country: 'Indonesia', cc: 'ID', region: 'asia', teams: [
    ['Persib Bandung', 'PSB'], ['Persija Jakarta', 'PSJ'], ['Arema FC', 'AFC'], ['Bali United', 'BAU'], ['Persebaya Surabaya', 'PSS'], ['PSM Makassar', 'PSM'] ] },
  { id: 'jleague', name: 'J1 League', country: 'Jepang', cc: 'JP', region: 'asia', teams: [
    ['Kawasaki Frontale', 'KAW'], ['Vissel Kobe', 'VIS'], ['Yokohama F. Marinos', 'YFM'], ['Urawa Reds', 'URA'], ['Cerezo Osaka', 'CER'], ['Sanfrecce Hiroshima', 'SAN'] ] },
  { id: 'saudi', name: 'Saudi Pro League', country: 'Arab Saudi', cc: 'SA', region: 'asia', teams: [
    ['Al Hilal', 'HIL'], ['Al Nassr', 'NAS'], ['Al Ittihad', 'ITT'], ['Al Ahli', 'AHL'], ['Al Shabab', 'SHA'], ['Al Ettifaq', 'ETT'] ] },
  { id: 'mls', name: 'Major League Soccer', country: 'Amerika Serikat', cc: 'US', region: 'am', teams: [
    ['LA Galaxy', 'LAG'], ['Inter Miami', 'MIA'], ['New York City FC', 'NYC'], ['Seattle Sounders', 'SEA'], ['Atlanta United', 'ATL'], ['Toronto FC', 'TOR'] ] },
  { id: 'brasileirao', name: 'Brasileirão Série A', country: 'Brasil', cc: 'BR', region: 'am', teams: [
    ['Flamengo', 'FLA'], ['Palmeiras', 'PAL'], ['Corinthians', 'COR'], ['São Paulo', 'SAO'], ['Santos', 'SAN'], ['Botafogo', 'BOT'] ] },
  { id: 'ligamx', name: 'Liga MX', country: 'Meksiko', cc: 'MX', region: 'am', teams: [
    ['Club América', 'AME'], ['Chivas', 'CHI'], ['Tigres UANL', 'TIG'], ['Monterrey', 'MTY'], ['Cruz Azul', 'CAZ'], ['Pumas UNAM', 'PUM'] ] },
  { id: 'intl', name: 'Pertandingan Internasional', country: 'Dunia', cc: 'UN', region: 'intl', teams: [
    ['Indonesia', 'IDN'], ['Jepang', 'JPN'], ['Brasil', 'BRA'], ['Argentina', 'ARG'], ['Prancis', 'FRA'], ['Spanyol', 'ESP'] ] },
];

export const LEAGUES = RAW.map((l) => ({
  id: l.id,
  name: l.name,
  country: l.country,
  countryCode: l.cc,
  region: l.region,
  slots: SLOTS[l.region],
  teams: l.teams.map(([name, short], k) => ({ id: `${l.id}-${k}`, name, short })),
}));

export const LEAGUE_BY_ID = new Map(LEAGUES.map((l) => [l.id, l]));
