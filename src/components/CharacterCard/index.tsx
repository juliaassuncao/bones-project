import type { CharacterCardProps } from './props';
import styles from './styles.module.scss';
export default function CharacterCard({ character: c, featured = false }: CharacterCardProps){return <article className={`${styles.card} ${featured ? styles.featured : ''}`}>
  <div className={styles.top}><span className={styles.motif}>{c.motif}</span><span className={styles.index}>{c.initials}</span></div>
  <div className={styles.center}><span aria-hidden="true">{c.initials}</span></div>
  <div className={styles.bottom}><p className={styles.role}>{c.role}</p><h3>{c.name}</h3><p className={styles.text}>{c.text}</p></div>
</article>}
