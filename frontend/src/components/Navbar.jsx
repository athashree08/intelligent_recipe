import React from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Navbar() {
    const { user, logout } = useAuth();

    return (
        <nav className="bg-cream/80 backdrop-blur-md sticky top-0 z-50 border-b border-olive/5">
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                <div className="flex justify-between items-center h-20">
                    {/* Logo */}
                    <Link to="/" className="flex items-center space-x-2 group">
                        <span className="text-3xl transition-transform group-hover:rotate-12 duration-300">🌿</span>
                        <span className="font-display font-bold text-2xl text-olive tracking-tight">
                            Snap2Serve
                        </span>
                    </Link>

                    {/* Navigation Links - Only show when logged in */}
                    {user && (
                        <div className="hidden md:flex items-center space-x-8">
                            <Link to="/" className="text-olive/70 hover:text-primary transition-colors font-medium font-display text-lg">
                                Home
                            </Link>
                            <Link to="/upload" className="text-olive/70 hover:text-primary transition-colors font-medium font-display text-lg">
                                Upload
                            </Link>
                            <Link to="/recipes" className="text-olive/70 hover:text-primary transition-colors font-medium font-display text-lg">
                                Recipes
                            </Link>
                            <Link to="/saved" className="text-olive/70 hover:text-primary transition-colors font-medium font-display text-lg">
                                Saved
                            </Link>
                        </div>
                    )}

                    {/* Auth Buttons */}
                    <div className="flex items-center space-x-4">
                        {user ? (
                            <>
                                <span className="text-sm text-olive/60 font-medium">Hi, {user.username}</span>
                                <button
                                    onClick={logout}
                                    className="text-sm text-secondary hover:text-secondary-dark transition-colors font-medium"
                                >
                                    Logout
                                </button>
                            </>
                        ) : (
                            <>
                                <Link to="/login" className="text-olive hover:text-primary transition-colors font-medium">
                                    Login
                                </Link>
                                <Link to="/signup" className="bg-olive text-cream px-6 py-2.5 rounded-full hover:bg-olive/90 transition-all shadow-lg shadow-olive/20 font-medium">
                                    Sign Up
                                </Link>
                            </>
                        )}
                    </div>
                </div>
            </div>
        </nav>
    );
}
