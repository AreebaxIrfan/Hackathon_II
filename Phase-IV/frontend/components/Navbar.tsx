'use client';

import React from 'react';
import Link from 'next/link';
import { useAuth } from '../lib/auth';

const Navbar = () => {
    const { user, isAuthenticated, logout } = useAuth();

    return (
        <nav className="bg-white shadow-sm border-b border-gray-200 py-4">
            <div className="max-w-4xl mx-auto px-4 flex justify-between items-center">
                <Link href="/" className="text-xl font-bold text-blue-600">
                    AI Todo Assistant
                </Link>

                <div className="flex items-center gap-4">
                    {isAuthenticated ? (
                        <>
                            <span className="text-sm text-gray-600 hidden md:inline">
                                {user?.email}
                            </span>
                            <button
                                onClick={logout}
                                className="text-sm bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg transition-colors"
                            >
                                Logout
                            </button>
                        </>
                    ) : (
                        <>
                            <Link
                                href="/auth/login"
                                className="text-sm text-gray-600 hover:text-blue-600 transition-colors"
                            >
                                Login
                            </Link>
                            <Link
                                href="/auth/register"
                                className="text-sm bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg transition-colors"
                            >
                                Register
                            </Link>
                        </>
                    )}
                </div>
            </div>
        </nav>
    );
};

export default Navbar;
