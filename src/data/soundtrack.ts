export type Track = {
  title: string;
  artist: string;
  chapter: number;
  note: string;
  url?: string;
};

// Faixas cuja presença foi conferida nas notas e no texto do PDF.
// Lista de destaques: não representa ainda um catálogo exaustivo de todas as menções.
export const tracks: Track[] = [
  {
    title: "Latch",
    artist: "Daniela Andrade",
    chapter: 20,
    note: "Indicação musical da autora.",
  },
  {
    title: "Nuvole Bianche",
    artist: "Ludovico Einaudi",
    chapter: 23,
    note: "Referência musical associada ao capítulo.",
  },
  {
    title: "Cursive",
    artist: "Billie Marten",
    chapter: 24,
    note: "Primeira música indicada pela autora.",
  },
  {
    title: "Clair de lune",
    artist: "Claude Debussy · Anne-Sophie Mutter · Lambert Orkis",
    chapter: 24,
    note: "Versão para violino e piano indicada pela autora.",
  },
  {
    title: "Say Yes to Heaven",
    artist: "Lana Del Rey",
    chapter: 25,
    note: "Primeira faixa indicada para a sequência musical.",
  },
  {
    title: "Ordinary",
    artist: "Alex Warren",
    chapter: 25,
    note: "Segunda faixa indicada para a sequência musical.",
  },
  {
    title: "TiO",
    artist: "ZAYN",
    chapter: 25,
    note: "Terceira faixa indicada para a sequência musical.",
  },
  {
    title: "Slip",
    artist: "Elliott Moss",
    chapter: 26,
    note: "Trilha indicada para a cena.",
  },
  {
    title: "We All Fall In Love Sometimes",
    artist: "Coldplay",
    chapter: 26,
    note: "Trilha indicada para a cena.",
  },
  {
    title: "O Fortuna",
    artist: "Carl Orff · Michael Tilson Thomas",
    chapter: 26,
    note: "Gravação indicada pela autora.",
  },
  {
    title: "Wicked Game",
    artist: "Daisy Gray",
    chapter: 26,
    note: "Versão específica indicada pela autora.",
  },
];
