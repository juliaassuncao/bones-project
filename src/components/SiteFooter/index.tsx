import { ArrowUpRight } from "lucide-react";
import { Link } from "react-router-dom";
import { SITE } from "../../constants/site";
import styles from "./styles.module.scss";
export default function SiteFooter() {
  return (
    <footer className={styles.footer}>
      <div className="container">
        <div className={styles.top}>
          <div>
            <span className={styles.title}>
              BONES<span>.</span>
            </span>
          </div>
          <div className={styles.links}>
            <Link to="/capitulos">Ler os capítulos</Link>
            <Link to="/trilha-sonora">Trilha sonora</Link>
            <a target="_blank" rel="noopener noreferrer" href={SITE.ao3}>
              Obra no AO3 <ArrowUpRight size={13} />
            </a>
          </div>
        </div>
        <div className={styles.bottom}>
          <div className={styles.credits}>
            <span>
              Uma história de{" "}
              <strong>
                <a
                  className={styles.creditLink}
                  href={SITE.x}
                  target="_blank"
                  rel="noopener noreferrer"
                  aria-label={`${SITE.author} no X (abre em nova aba)`}
                >
                  {SITE.author}
                </a>
              </strong>
              . Conteúdo e personagens pertencem aos respectivos criadores.
            </span>
            <p className={styles.webCredit}>
              Criação e desenvolvimento web por{" "}
              <a
                className={styles.creditLink}
                href={SITE.creatorX}
                target="_blank"
                rel="noopener noreferrer"
                aria-label={`${SITE.creator} no X (abre em nova aba)`}
              >
                {SITE.creator}
              </a>
            </p>
          </div>
          <span>FAN PROJECT · SEM FINS COMERCIAIS</span>
        </div>
      </div>
    </footer>
  );
}
