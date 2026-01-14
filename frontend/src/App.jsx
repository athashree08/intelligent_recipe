import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Upload from './pages/Upload';
import RecipeList from './pages/RecipeList';
import RecipeDetail from './pages/RecipeDetail';
import SavedRecipes from './pages/SavedRecipes';

function App() {
    return (
        <AuthProvider>
            <Router>
                <Navbar />
                <Routes>
                    <Route path="/" element={<Home />} />
                    <Route path="/login" element={<Login initialMode="login" />} />
                    <Route path="/signup" element={<Login initialMode="signup" />} />
                    <Route path="/upload" element={<Upload />} />
                    <Route path="/recipes" element={<RecipeList />} />
                    <Route path="/recipe/:id" element={<RecipeDetail />} />
                    <Route path="/saved" element={<SavedRecipes />} />
                </Routes>
            </Router>
        </AuthProvider>
    );
}

export default App;
