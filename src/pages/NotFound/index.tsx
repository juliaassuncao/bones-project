import { Link } from 'react-router-dom';
import styles from './styles.module.scss';
export default function NotFound(){return <div className={styles.page}><span className="eyebrow">REGISTRO NÃO ENCONTRADO</span><h1>404.</h1><p>Esta página não faz parte do arquivo.</p><Link className="button" to="/">VOLTAR PARA O INÍCIO</Link></div>}
