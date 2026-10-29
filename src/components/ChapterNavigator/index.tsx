import { Link } from 'react-router-dom';
import { ArrowLeft, ArrowRight } from 'lucide-react';
import { chapterHref } from '../../data/chapters';
import type { ChapterNavigatorProps } from './props';
import styles from './styles.module.scss';
export default function ChapterNavigator({previous,next,showLabel=true}:ChapterNavigatorProps){return <nav aria-label="Navegação entre capítulos" className={styles.nav}><div>{previous&&<Link to={chapterHref(previous)}><ArrowLeft size={18}/><span>{showLabel&&<small>CAPÍTULO ANTERIOR</small>}{previous.title}</span></Link>}</div><div>{next&&<Link to={chapterHref(next)}><span>{showLabel&&<small>PRÓXIMO CAPÍTULO</small>}{next.title}</span><ArrowRight size={18}/></Link>}</div></nav>}
