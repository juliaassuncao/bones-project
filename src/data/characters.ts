export type Character = {
  name: string;
  role: string;
  initials: string;
  text: string;
  group: "principal" | "apoio";
  motif: string;
};

// Fichas deliberadamente limitadas ao que está claro nos primeiros capítulos.
// Não revelam passado, mistérios nem resoluções posteriores.
export const characters: Character[] = [
  {
    name: "Eduarda Fragoso",
    role: "A antropóloga",
    initials: "EF",
    group: "principal",
    motif: "RAZÃO / MÉTODO",
    text: "PhD em antropologia forense, superintendente da Polícia Federal e nova professora na USP. Uma inteligência extraordinária que confia nas evidências, na lógica e naquilo que pode ser comprovado.",
  },
  {
    name: "Lorena Ferette",
    role: "A estudante",
    initials: "LF",
    group: "principal",
    motif: "ESCUTA / INTUIÇÃO",
    text: "Concluinte de psicologia na USP, atenciosa e observadora. Sua curiosidade e sua capacidade de enxergar além dos fatos a colocam diante de uma professora tão fascinante quanto difícil de compreender.",
  },
  {
    name: "Angélica",
    role: "A avó",
    initials: "A",
    group: "apoio",
    motif: "CUIDADO / MEMÓRIA",
    text: "Avó de Lorena, psicóloga renomada e antiga professora de Eduarda. Seu afeto e sua experiência fazem dela um elo importante entre as duas.",
  },
  {
    name: "Cristine",
    role: "A filha",
    initials: "C",
    group: "apoio",
    motif: "AFETO / FAMÍLIA",
    text: "Filha de Eduarda, curiosa, carinhosa e apaixonada por aprender. É uma das pessoas capazes de revelar um lado menos conhecido da antropóloga.",
  },
  {
    name: "Paulo “Paulinho” Reitz",
    role: "O escritor",
    initials: "PR",
    group: "apoio",
    motif: "FAMÍLIA / PASSADO",
    text: "Escritor e pai de Cristine. Compartilha com Eduarda os desafios e as responsabilidades da criação da filha.",
  },
  {
    name: "Viviane",
    role: "A amiga",
    initials: "V",
    group: "apoio",
    motif: "HUMOR / AMIZADE",
    text: "Amiga de Lorena na faculdade. Espontânea e bem-humorada, costuma arrancar risadas do grupo mesmo nos momentos mais tensos.",
  },
  {
    name: "Júnior, Ana e Maggye",
    role: "A equipe",
    initials: "α",
    group: "apoio",
    motif: "CIÊNCIA / CONFIANÇA",
    text: "Profissionais do núcleo forense da Polícia Federal e parte do círculo de confiança de Eduarda, cada um com sua especialidade.",
  },
];
