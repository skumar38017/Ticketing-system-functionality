import React from "react";

export function GridSmallBackgroundDemo({ children }) {
  return (
    <div className=" w-full  h-full  dark:sm:bg-grid-small-white/[0.05] dark:bg-grid-small-white/[0.01] bg-grid-small-black/[0.2] relative ">
      {/* Radial gradient for the container to give a faded look */}
      <div className="absolute pointer-events-none inset-0 flex items-center justify-center   [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]"></div>

      {children}
    </div>
  );
}
