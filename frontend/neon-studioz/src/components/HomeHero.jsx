import React from "react";
import { TfiMouse } from "react-icons/tfi";

function HomeHero({ onScrollDown }) {
  return (
    <div className="max-h-screen flex flex-col items-center justify-center px-4 sm:px-6 md:px-8 lg:px-12 xl:px-16 py-4 w-full gap-4">
      <div className="w-full max-w-5xl flex items-center justify-center px-4 sm:px-8 md:px-12 lg:px-16 py-4">
        <video
          src={"./NeonLogoVid.mp4"}
          autoPlay
          loop
          muted
          className="w-[650px]"
        />
      </div>
      <div className="flex flex-col items-center justify-center">
        {/* Mouse Icon with animation */}
        <TfiMouse
          size={35}
          className="cursor-pointer animate-bounce mb-4 text-white"
          onClick={onScrollDown}
        />
        {/* Scroll Down text with animation */}
        <p className="text-white text-base sm:text-lg md:text-xl lg:text-2xl font-semibold animate-fadeInUp">
          Scroll Down
        </p>
      </div>
    </div>
  );
}

export default HomeHero;
