import type { SectionHeadingProps } from './props';
import styles from './styles.module.scss';
export default function SectionHeading({label,title,description,action}:SectionHeadingProps){return <div className={styles.wrap}><div><span className="eyebrow">{label}</span><h2>{title}</h2>{description && <p>{description}</p>}</div>{action && <div>{action}</div>}</div>}
