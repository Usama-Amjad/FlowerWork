import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Account from "./pages/Account";
import Navbar from "./components/Navbar";
import { Route, Routes } from "react-router-dom";
import { AuthContextProvider } from "./context/AuthContext";
import ProtectedRoute from './components/ProtectedRoute'; 
import Player from "./pages/Player";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

function App() {
  return (
    <>
      <AuthContextProvider>
      <Navbar />
      <ToastContainer theme="dark"/>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/player/:id" element={<Player />} />
        <Route path="/account" element={<ProtectedRoute> <Account /></ProtectedRoute>} />
      </Routes>
      </AuthContextProvider>
    </>
  );
}

export default App;
