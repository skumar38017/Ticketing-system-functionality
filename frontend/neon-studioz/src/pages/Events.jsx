// pages/Events.jsx
import React from "react";
import { GridSmallBackgroundDemo } from "@/components/ui/GridSmallBackgroundDemo";
import { Spotlight } from "@/components/ui/spotlight-new";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";
import NeonOrganizers from "../components/NeonOrganizers";
import Canvas from "../components/Canvas";

const Events = () => {
  return (
    <div className="bg-black h-full w-full max-w-[1600px]">
      <GridSmallBackgroundDemo>
        <Navbar />
        <Spotlight />
        <div className="flex flex-col w-full items-center justify-center">
          {/* <div className="w-full h-0.5 border-t my-10 border-gray-300 opacity-50 sm:max-w-2xl lg:max-w-4xl xl:max-w-6xl max-w-xs"></div> */}
          <Footer />
        </div>
      </GridSmallBackgroundDemo>
    </div>
  );
};

export default Events;
