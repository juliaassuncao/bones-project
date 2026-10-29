import { useEffect, useState } from 'react';
import { Link, NavLink, useLocation } from 'react-router-dom';
import { Menu, X } from 'lucide-react';
import { NAVIGATION } from '../../constants/site';
import styles from './styles.module.scss';

export default function SiteHeader() {
  const [open, setOpen] = useState(false);
  const { pathname } = useLocation();
  useEffect(() => { setOpen(false); }, [pathname]);
  return (
    <header className={styles.header}>
      <div className={`${styles.inner} container`}>
        <Link className={styles.brand} to="/" aria-label="Bones — voltar ao início">
          <span className={styles.monogram}>B<span>.</span></span>
          <span className={styles.brandCopy}><strong>BONES</strong><small>ARQUIVO VIVO</small></span>
        </Link>
        <nav className={`${styles.nav} ${open ? styles.open : ''}`} aria-label="Navegação principal" id="primary-navigation">
          {NAVIGATION.map(({ label, to }) => <NavLink key={to} to={to} end={to === '/'} className={({ isActive }) => `${styles.link} ${isActive ? styles.active : ''}`}>{label}</NavLink>)}
        </nav>
        <Link className={styles.readLink} to="/capitulos">LER A FIC <span aria-hidden="true">↗</span></Link>
        <button className={styles.menu} onClick={() => setOpen(v => !v)} aria-expanded={open} aria-controls="primary-navigation" aria-label={open ? 'Fechar menu' : 'Abrir menu'}>{open ? <X size={24}/> : <Menu size={24}/>}</button>
      </div>
    </header>
  );
}
