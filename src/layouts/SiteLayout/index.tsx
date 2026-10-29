import { Outlet, useLocation } from 'react-router-dom';
import { useEffect } from 'react';
import SiteHeader from '../../components/SiteHeader';
import SiteFooter from '../../components/SiteFooter';
export default function SiteLayout(){const {pathname}=useLocation();useEffect(()=>{window.scrollTo({top:0,behavior:'auto'});},[pathname]);return <><a href="#main" className="skipLink">Ir para o conteúdo</a><SiteHeader/><main id="main"><Outlet/></main><SiteFooter/></>}
