import React, { useState } from "react";
import { Link } from "react-router-dom";
import { Menu, X } from "lucide-react";

const Navbar = () => {
  const [isMenuOpen, setIsMenuOpen] = useState(false);

  const toggleMenu = () => setIsMenuOpen(!isMenuOpen);
  const closeMenu = () => setIsMenuOpen(false);

  return (
    <div className="h-[6.5rem] relative z-50">
      <div className="flex items-center justify-center h-full w-full backdrop-blur-sm">
        <div className="w-full text-gray-700">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 flex justify-between items-center w-full">
            {/* Logo */}
            <Link to="/" className="">
              <div className="gap-2 flex items-center justify-center ">
                <img src="./neonlogo.png" alt="logo" className="size-20" />
                <span className="text-2xl sm:text-3xl md:text-4xl tracking-widest uppercase rounded-lg text-white focus:outline-none focus:shadow-outline font-custom hover:scale-105  duration-500">
                  NEON STUDIOZ
                </span>
              </div>
            </Link>

            {/* Desktop Navigation */}
            <div className="hidden lg:flex lg:space-x-16 font-roboto font-light text-xl md:text-2xl">
              <Link
                to="/"
                className="relative inline-block text-gray-200 hover:text-cyan-500 md:mt-0 md:ml-4 transition-all duration-300 transform hover:scale-110 group"
                onClick={closeMenu}
              >
                HOME
                <span className="absolute left-0 right-0 bottom-0 h-[2px] bg-cyan-600 scale-x-0 transition-transform duration-300 group-hover:scale-x-100 origin-left"></span>
              </Link>
              <Link
                to="/events"
                className="relative inline-block text-gray-200 hover:text-cyan-500 md:mt-0 md:ml-4 transition-all duration-300 transform hover:scale-110 group"
                onClick={closeMenu}
              >
                EVENTS
                <span className="absolute left-0 right-0 bottom-0 h-[2px] bg-cyan-600 scale-x-0 transition-transform duration-300 group-hover:scale-x-100 origin-left"></span>
              </Link>

              <Link
                to="/contactus"
                className="relative inline-block text-gray-200 hover:text-cyan-500 md:mt-0 md:ml-4 transition-all duration-300 transform hover:scale-110 group"
                onClick={closeMenu}
              >
                CONTACT US
                <span className="absolute left-0 right-0 bottom-0 h-[2px] bg-cyan-600 scale-x-0 transition-transform duration-300 group-hover:scale-x-100 origin-left"></span>
              </Link>
            </div>

            {/* Hamburger Menu Button */}
            <button
              onClick={toggleMenu}
              className="block lg:hidden text-white p-2 rounded-lg hover:bg-white/10 transition-all duration-300"
              aria-label="Toggle Menu"
            >
              {isMenuOpen ? (
                <X className="w-8 h-8" />
              ) : (
                <Menu className="w-8 h-8" />
              )}
            </button>
          </div>

          {/* Mobile Navigation Menu */}
          <div
            className={`fixed inset-x-0 top-[7rem] transform lg:hidden transition-all duration-300 ease-in-out ${
              isMenuOpen
                ? "translate-y-0 opacity-100 visible"
                : "-translate-y-full opacity-0 invisible"
            }`}
          >
            <div className="bg-black bg-opacity-90 shadow-lg mx-4 rounded-xl overflow-hidden">
              <div className="px-4 py-6 space-y-4">
                <Link
                  to="/"
                  className="block py-3 px-4  text-gray-200 hover:text-cyan-500 hover:underline hover:underline-offset-4 rounded-lg transition-all duration-300"
                  onClick={closeMenu}
                >
                  <span className="text-lg font-light">HOME</span>
                </Link>
                <Link
                  to="/contact"
                  className="block py-3 px-4 text-gray-200 hover:text-cyan-500 hover:underline hover:underline-offset-4 rounded-lg transition-all duration-300"
                  onClick={closeMenu}
                >
                  <span className="text-lg font-light">CONTACT</span>
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Divider Line */}
      <div className="flex items-center justify-center w-full">
        <div className="w-full border-2 border-gray-300 opacity-80 sm:max-w-2xl lg:max-w-4xl xl:max-w-6xl max-w-xs"></div>
      </div>
    </div>
  );
};

export default Navbar;
