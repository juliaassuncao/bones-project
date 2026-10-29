export type ContentBlock =
  | { type: 'paragraph' | 'pov' | 'dateline' | 'music-cue' | 'aside'; html: string }
  | { type: 'divider' }
  | { type: 'image'; src: string; alt: string };

export type ChapterData = {
  number: number;
  title: string;
  slug: string;
  source: { startPage: number; endPage: number };
  summary: ContentBlock[];
  notes: ContentBlock[];
  content: ContentBlock[];
  endNotes: ContentBlock[];
  images: string[];
};

export type ChapterMeta = {
  number: number;
  title: string;
  slug: string;
  startPage: number;
  endPage: number;
  hasNotes: boolean;
  hasImages: boolean;
  readingBlocks: number;
};

export type ReadingPreferences = {
  theme: 'paper' | 'night';
  font: 'serif' | 'sans';
  size: number;
  lineHeight: number;
};
