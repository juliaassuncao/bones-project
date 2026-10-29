import type { ArchiveLabelProps } from './props';
import styles from './styles.module.scss';
export default function ArchiveLabel({number,label,light=false}:ArchiveLabelProps){return <div className={`${styles.label} ${light ? styles.light : ''}`}><span>{number}</span><span className={styles.rule}/><span>{label}</span></div>}
