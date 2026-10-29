import type { CSSProperties } from 'react';
import type { ChapterBodyProps } from './props';
import styles from './styles.module.scss';
import { SITE } from '../../constants/site';
export default function ChapterBody({blocks,preferences,kind='body'}:ChapterBodyProps){
  const vars={'--reading-size':`${preferences.size}px`,'--reading-line':String(preferences.lineHeight)} as CSSProperties;
  return <div style={vars} className={`${styles.body} ${preferences.theme==='night'?styles.night:styles.paper} ${preferences.font==='sans'?styles.sans:styles.serif} ${kind==='note'?styles.note:''}`}>
    {blocks.map((b,i)=>{
      if(b.type==='divider') return <div key={i} className={styles.divider} aria-label="Mudança de cena"><span>✳</span></div>;
      if(b.type==='image') return <figure key={i} className={styles.figure}><img src={b.src} alt={b.alt} loading="lazy" /></figure>;
      if (b.type==='music-cue') return <div key={i} className={styles.music}><p dangerouslySetInnerHTML={{__html:b.html}}/><a href={SITE.spotify} target="_blank" rel="noopener noreferrer">ABRIR PLAYLIST OFICIAL ↗</a></div>;
      const className=b.type==='pov'?styles.pov:b.type==='dateline'?styles.dateline:b.type==='aside'?styles.aside:styles.paragraph;
      // Conteúdo HTML é gerado pelo importador local: o texto é escapado na extração
      // e somente <em>/<strong> são produzidos, sem markup arbitrário do PDF.
      return <p key={i} className={className} dangerouslySetInnerHTML={{__html:b.html}}/>;
    })}
  </div>
}
