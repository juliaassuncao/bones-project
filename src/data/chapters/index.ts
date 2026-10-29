import type { ChapterData, ChapterMeta } from '../../types/content';
import manifest from './manifest.json';

export const chapters: ChapterMeta[] = manifest as ChapterMeta[];

const chapterModules = import.meta.glob('./[0-9][0-9].json');

export async function getChapter(number: number): Promise<ChapterData> {
  const path = `./${String(number).padStart(2, '0')}.json`;
  const loader = chapterModules[path];
  if (!loader) throw new Error(`Capítulo ${number} não encontrado`);
  const mod = (await loader()) as { default: ChapterData };
  return mod.default;
}

export function chapterHref(meta: Pick<ChapterMeta, 'slug'>): string {
  return `/capitulos/${meta.slug}`;
}
