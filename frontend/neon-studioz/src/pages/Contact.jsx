// pages/Home.jsx
import React from "react";
import { GridSmallBackgroundDemo } from "@/components/ui/GridSmallBackgroundDemo";
import { Spotlight } from "@/components/ui/spotlight-new";
import Navbar from "../components/Navbar";
import Footer from "../components/Footer";

const Contact = () => {
  return (
    <div className="bg-black h-full w-full max-w-[1600px]">
      <GridSmallBackgroundDemo>
        <Navbar />
        <Spotlight />
        <div className="flex flex-col w-full items-center justify-center">
          <h1 className="text-white text-5xl font-bold">Contact</h1>
          <Footer />
        </div>
      </GridSmallBackgroundDemo>
    </div>
  );
};

export default Contact;
