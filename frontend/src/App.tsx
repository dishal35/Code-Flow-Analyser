import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import GraphPage from './pages/GraphPage';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<div>Home</div>} />
        <Route path="/graph" element={<GraphPage />} />
      </Routes>
    </Router>
  );
}

export default App
