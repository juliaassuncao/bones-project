import { ArrowUpRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { SITE } from '../../constants/site';
import styles from './styles.module.scss';
export default function SiteFooter(){return <footer className={styles.footer}>
  <div className="container"><div className={styles.top}><div><span className={styles.title}>BONES<span>.</span></span><p>Algumas marcas não podem ser medidas.</p></div><div className={styles.links}><Link to="/capitulos">Ler os capítulos</Link><Link to="/trilha-sonora">Trilha sonora</Link><a target="_blank" rel="noopener noreferrer" href={SITE.ao3}>Obra no AO3 <ArrowUpRight size={13}/></a></div></div>
  <div className={styles.bottom}><span>Uma história de <strong>{SITE.author}</strong>. Conteúdo e personagens pertencem aos respectivos criadores.</span><span>FAN PROJECT · SEM FINS COMERCIAIS</span></div></div>
</footer>}
