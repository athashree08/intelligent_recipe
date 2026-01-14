import React, { useEffect, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export default function Home() {
    const { user } = useAuth();
    const location = useLocation();
    const [welcomeMessage, setWelcomeMessage] = useState('');

    useEffect(() => {
        if (location.state?.message) {
            setWelcomeMessage(location.state.message);
            // Clear message from state so it doesn't persist on refresh/back
            window.history.replaceState({}, document.title);
        }
    }, [location]);

    // If user is logged in, show the Dashboard/Normal Working capability
    if (user) {
        return (
            <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
                {welcomeMessage && (
                    <div className="bg-primary/20 text-olive px-6 py-4 rounded-xl mb-8 border border-primary/30 flex items-center justify-between animate-fade-in-up">
                        <span className="font-medium text-lg">{welcomeMessage}</span>
                        <button onClick={() => setWelcomeMessage('')} className="text-olive/60 hover:text-olive">✕</button>
                    </div>
                )}

                <div className="text-center mb-16">
                    <span className="font-display italic text-2xl text-secondary block mb-2">My Kitchen</span>
                    <h1 className="font-display font-bold text-5xl text-olive mb-4">
                        Dashboard
                    </h1>
                    <p className="text-xl text-olive/80 font-light">Ready to create something delicious?</p>
                </div>

                <div className="grid md:grid-cols-2 gap-8 max-w-4xl mx-auto">
                    <Link to="/upload" className="bg-white p-10 rounded-[30px] shadow-sm hover:shadow-xl transition-all duration-500 text-center group border border-stone-100 hover:-translate-y-2">
                        <div className="text-6xl mb-6 transform group-hover:scale-110 transition-transform duration-500 opacity-80">📸</div>
                        <h2 className="font-display font-bold text-3xl text-olive mb-3">Snap Ingredients</h2>
                        <p className="text-olive/70 font-light text-lg">Take a photo of your pantry to find recipes instantly</p>
                    </Link>

                    <Link to="/recipes" className="bg-white p-10 rounded-[30px] shadow-sm hover:shadow-xl transition-all duration-500 text-center group border border-stone-100 hover:-translate-y-2">
                        <div className="text-6xl mb-6 transform group-hover:scale-110 transition-transform duration-500 opacity-80">📖</div>
                        <h2 className="font-display font-bold text-3xl text-olive mb-3">My Cookbook</h2>
                        <p className="text-olive/70 font-light text-lg">Browse your generated recipes and saved favorites</p>
                    </Link>
                </div>
            </div>
        );
    }

    // Landing Page for Non-Logged In Users
    return (
        <div className="min-h-screen bg-cream relative overflow-hidden">
            {/* Background Decorations */}
            <div className="absolute top-0 right-0 w-1/3 h-full bg-stone-100/50 -z-10 rounded-l-[100px] hidden md:block"></div>

            {/* Hero Section */}
            <section className="pt-24 pb-32">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center max-w-4xl mx-auto relative z-10">
                        <div className="mb-8 flex justify-center space-x-6 text-4xl opacity-40 animate-float-slow">
                            <span>🧄</span>
                            <span>🌿</span>
                            <span>🍅</span>
                        </div>

                        <h1 className="font-display text-7xl md:text-8xl text-olive mb-6 leading-tight">
                            Snap2Serve
                            <div className="text-3xl md:text-4xl italic text-secondary mt-4 font-normal">
                                Handpicked by AI, inspired by home
                            </div>
                        </h1>

                        <div className="w-24 h-1 bg-primary/40 mx-auto my-10 rounded-full"></div>

                        <p className="text-xl text-olive/70 mb-12 max-w-2xl mx-auto font-light leading-relaxed">
                            Experience the joy of cooking without the hassle of planning.
                            Simply snap a photo of your ingredients, and let our intelligent kitchen assistant craft the perfect recipe for you.
                        </p>

                        <div className="flex flex-col sm:flex-row gap-6 justify-center">
                            <Link to="/signup" className="btn-primary text-lg px-12 py-4 rounded-full font-display tracking-wide shadow-lg shadow-primary/20 hover:shadow-xl transition-all hover:-translate-y-1">
                                Get Started
                            </Link>
                            <Link to="/login" className="btn-secondary text-lg px-12 py-4 rounded-full font-display tracking-wide border-olive/20 text-olive hover:bg-stone-100">
                                Log In
                            </Link>
                        </div>
                    </div>
                </div>
            </section>

            {/* Featured Section */}
            <section className="py-24 bg-white/50 backdrop-blur-sm rounded-t-[60px] border-t border-stone-100">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="text-center mb-16">
                        <h2 className="font-display text-4xl text-olive mb-4">Fresh Inspirations</h2>
                        <p className="text-secondary italic font-display text-xl">Curated just for you</p>
                    </div>

                    <div className="grid md:grid-cols-3 gap-10">
                        {/* Styled Cards */}
                        {[
                            { title: 'Roasted Vegetable Medley', time: '45 min', img: '🥕', desc: 'A rustic blend of root vegetables' },
                            { title: 'Fresh Basil Pesto', time: '15 min', img: '🌿', desc: 'Aromatic and vibrant green sauce' },
                            { title: 'Artisan Bead Soup', time: '30 min', img: '🍲', desc: 'Warm comfort in a bowl' }
                        ].map((item, i) => (
                            <div key={i} className="bg-cream rounded-[30px] p-8 border border-stone-100 hover:shadow-xl transition-all duration-300 group cursor-default">
                                <div className="h-48 rounded-[20px] bg-stone-100 flex items-center justify-center text-8xl mb-6 group-hover:scale-[1.02] transition-transform duration-500 relative overflow-hidden">
                                    <span className="drop-shadow-sm">{item.img}</span>
                                    <div className="absolute inset-0 bg-gradient-to-t from-black/5 to-transparent"></div>
                                </div>
                                <h3 className="font-display text-2xl text-olive mb-2 group-hover:text-primary transition-colors">{item.title}</h3>
                                <p className="text-olive/60 font-light mb-4 text-sm">{item.desc}</p>
                                <div className="flex items-center justify-between pt-4 border-t border-stone-200/50">
                                    <span className="text-secondary font-medium text-sm tracking-wide">Ready in {item.time}</span>
                                    <span className="w-8 h-8 rounded-full bg-white flex items-center justify-center text-primary border border-stone-100 shadow-sm">➜</span>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            </section>
        </div>
    );
}
