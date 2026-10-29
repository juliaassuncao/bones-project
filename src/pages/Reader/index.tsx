import { useEffect, useState } from 'react';
import { useNavigate, useParams, Link } from 'react-router-dom';
import { ArrowLeft, ArrowUpRight, Check, ChevronDown, BookOpen, SlidersHorizontal } from 'lucide-react';
import ArchiveLabel from '../../components/ArchiveLabel';
import ChapterBody from '../../components/ChapterBody';
import ChapterNavigator from '../../components/ChapterNavigator';
import ReadingControls from '../../components/ReadingControls';
import ScrollProgress from '../../components/ScrollProgress';
import { chapterHref, chapters, getChapter } from '../../data/chapters';
import type { ChapterData } from '../../types/content';
import { useChapterProgress } from '../../hooks/useChapterProgress';
import { useReadingPreferences } from '../../hooks/useReadingPreferences';
import { SITE } from '../../constants/site';
import styles from './styles.module.scss';
export default function Reader(){
  const {slug}=useParams(); const navigate=useNavigate();
  const meta=chapters.find(c=>c.slug===slug);
  const [data,setData]=useState<ChapterData | null>(null);
  const [error,setError]=useState(false);
  const [showPrefs,setShowPrefs]=useState(false);
  const {prefs,update}=useReadingPreferences();
  const {finished,toggle}=useChapterProgress();
  useEffect(()=>{if(!meta){setData(null);return;}let alive=true;setData(null);setError(false);getChapter(meta.number).then(ch=>{if(alive)setData(ch)}).catch(()=>{if(alive)setError(true)});return()=>{alive=false}},[meta?.number]);
  useEffect(()=>{document.title=meta?`${meta.title} · Bones`:'Capítulo não encontrado · Bones';return()=>{document.title='Bones — Arquivo Vivo'}},[meta]);
  if(!meta)return <div className={`${styles.error} container`}><h1>Registro não encontrado.</h1><Link to="/capitulos">Voltar para o índice</Link></div>;
  const prev=chapters.find(c=>c.number===meta.number-1);const next=chapters.find(c=>c.number===meta.number+1);
  const marked=finished.includes(meta.number);
  return <div className={styles.reader}><ScrollProgress/><div className="container">
    <div className={styles.toolbar}><Link to="/capitulos" className={styles.back}><ArrowLeft size={16}/> ÍNDICE DE CAPÍTULOS</Link><div className={styles.tools}><label htmlFor="chapter-picker" className={styles.picker}><BookOpen size={16}/><span>CAP. {String(meta.number).padStart(2,'0')}</span><ChevronDown size={14}/></label><select id="chapter-picker" className={styles.select} value={meta.number} onChange={e=>{const c=chapters.find(c=>c.number===Number(e.target.value));if(c)navigate(chapterHref(c))}} aria-label="Escolher capítulo">{chapters.map(c=><option key={c.number} value={c.number}>{String(c.number).padStart(2,'0')} · {c.title}</option>)}</select><button type="button" className={`${styles.settings} ${showPrefs?styles.active:''}`} onClick={()=>setShowPrefs(v=>!v)} aria-expanded={showPrefs} aria-controls="reading-preferences"><SlidersHorizontal size={16}/> AJUSTES</button></div></div>
    {showPrefs&&<div id="reading-preferences" className={styles.prefs}><ReadingControls value={prefs} onChange={update}/></div>}
    <header className={styles.chapterTitle}><ArchiveLabel number={`REGISTRO ${String(meta.number).padStart(3,'0')}`} label="BONES / MARYDEBONES"/><h1>{meta.title}</h1><div className={styles.chapterLine}><span>CAPÍTULO {meta.number} DE {chapters.length}</span><span>ARQUIVO ORIGINAL · PÁGS. {meta.startPage}–{meta.endPage}</span></div></header>
    {error&&<div className={styles.loading}>Não foi possível carregar o capítulo. <button onClick={()=>window.location.reload()}>Tentar novamente</button></div>}
    {!data&&!error&&<div className={styles.loading} role="status">Abrindo registro...</div>}
    {data&&<>
      {(data.summary.length>0||data.notes.length>0)&&<div className={styles.prefatory}><div className={styles.noteTitle}>NOTAS ANTES DA LEITURA</div>{data.summary.length>0&&<ChapterBody blocks={data.summary} preferences={prefs} kind="note"/>}{data.notes.length>0&&<ChapterBody blocks={data.notes} preferences={prefs} kind="note"/>}</div>}
      <article className={styles.paper} aria-label={`Texto completo do capítulo ${meta.number}`}><ChapterBody blocks={data.content} preferences={prefs}/></article>
      {data.endNotes.length>0&&<section className={styles.endnotes}><div className={styles.noteTitle}>NOTAS DA AUTORA · FINAL DO CAPÍTULO</div><ChapterBody blocks={data.endNotes} preferences={prefs} kind="note"/></section>}
      <div className={styles.after}><button type="button" className={`${styles.mark} ${marked?styles.marked:''}`} onClick={()=>toggle(meta.number)} aria-pressed={marked}>{marked?<Check size={17}/>:<BookOpen size={17}/>} {marked?'CAPÍTULO MARCADO COMO LIDO':'MARCAR CAPÍTULO COMO LIDO'}</button><p>Marcação salva somente neste navegador.</p></div>
      <ChapterNavigator previous={prev} next={next}/><div className={styles.bottom}><a href={SITE.ao3} target="_blank" rel="noopener noreferrer">VISITAR A FIC ORIGINAL NO AO3 <ArrowUpRight size={15}/></a><Link to="/capitulos">VER TODOS OS CAPÍTULOS</Link></div>
    </>}
  </div></div>}
