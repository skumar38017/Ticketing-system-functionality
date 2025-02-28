import React, { useRef } from "react";
import HomeHero from "../components/HomeHero";
import NeonDescription from "./NeonDescription";

function Canvas() {
  const nextSectionRef = useRef(null);

  const handleScrollDown = () => {
    if (nextSectionRef.current) {
      nextSectionRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <>
      {/* Hero Section */}
      <div className="relative z-10 w-full lg:min-h-screen max-h-screen flex flex-col items-center justify-center">
        <HomeHero onScrollDown={handleScrollDown} />
      </div>

      {/* Next Section - NeonDescription */}
      <div
        ref={nextSectionRef}
        className="relative z-10 flex flex-col items-center justify-center w-full min-h-screen mt-2"
      >
        {/* SVG Section */}
        <div className="relative w-full h-16 sm:h-24 md:h-32 lg:h-40">
          <svg
            className="absolute top-0 left-0 w-full h-full"
            viewBox="0 0 100 20"
            preserveAspectRatio="none"
          >
            <polygon points="0,20 75,0 100,20" fill="white" />
          </svg>
        </div>

        {/* White Section Below */}
        <div className="flex-grow w-full bg-white px-4 sm:px-8 md:px-12 lg:px-20 xl:px-32">
          <NeonDescription />
        </div>
      </div>
    </>
  );
}

export default Canvas;