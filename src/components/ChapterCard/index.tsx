import { Link } from 'react-router-dom';
import { ArrowUpRight, Check } from 'lucide-react';
import { chapterHref } from '../../data/chapters';
import type { ChapterCardProps } from './props';
import styles from './styles.module.scss';
export default function ChapterCard({chapter,finished}:ChapterCardProps){return <Link className={styles.card} to={chapterHref(chapter)}><span className={styles.number}>{String(chapter.number).padStart(3,'0')}</span><span className={styles.main}><span className={styles.micro}>REGISTRO {String(chapter.number).padStart(2,'0')} {finished && <span className={styles.finished}><Check size={11}/> CONCLUÍDO</span>}</span><strong>{chapter.title}</strong></span><ArrowUpRight className={styles.arrow} size={21}/></Link>}
