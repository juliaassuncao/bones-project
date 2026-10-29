import { Route, Routes } from 'react-router-dom';
import SiteLayout from './layouts/SiteLayout';
import Home from './pages/Home';
import About from './pages/About';
import Characters from './pages/Characters';
import Chapters from './pages/Chapters';
import Soundtrack from './pages/Soundtrack';
import Reader from './pages/Reader';
import NotFound from './pages/NotFound';

export default function App() {
  return (
    <Routes>
      <Route element={<SiteLayout />}>
        <Route index element={<Home />} />
        <Route path="sobre" element={<About />} />
        <Route path="personagens" element={<Characters />} />
        <Route path="capitulos" element={<Chapters />} />
        <Route path="trilha-sonora" element={<Soundtrack />} />
        <Route path="capitulos/:slug" element={<Reader />} />
        <Route path="*" element={<NotFound />} />
      </Route>
    </Routes>
  );
}
