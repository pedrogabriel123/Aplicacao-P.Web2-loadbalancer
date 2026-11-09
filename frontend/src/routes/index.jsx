import { BrowserRouter, Routes, Route } from "react-router-dom";
import Produtores from "../pages/Produtores";

export default function Router() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Produtores />} />
      </Routes>
    </BrowserRouter>
  );
}
