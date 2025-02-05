import React from "react";

function NeonDescription() {
  return (
    <main className="flex items-center justify-center w-full sm:min-h-screen px-2 sm:px-6 lg:px-8 ">
      <div className="grid sm:gap-8 gap-2 w-full max-w-7xl lg:px-6 px-4 p-8">
        {/* Title Section */}
        <h2
          className="text-3xl sm:text-4xl md:text-5xl font-black text-center  mb-8 font-brush-king"
          style={{
            color: "#fcfcfc",
            WebkitTextStroke: "2px #0197D4",
            // textShadow: "0 0 20px #0197D4",
          }}
        >
          <div className="flex lg:flex-row flex-col items-center justify-center lg:gap-16 md:gap-12 gap-6">
            <p>NEON</p>
            <p>STUDIOZ</p>
          </div>
        </h2>

        {/* Grid Layout for Content */}
        <div className="grid md:grid-cols-3 gap-8 items-center sm:p-4 p-4 ">
          {/* Image Section */}
          <div className=" place-items-center p-4 hidden sm:grid  w-full flex items-center justify-center">
            <img
              src="/neonlogocircle.png" // Ensure the path is correct
              alt="Neon Logo"
              className="w-32 sm:w-40 md:w-56 lg:w-72 aspect-square rounded-full ring-4 ring-pink-600"
              style={{
                borderColor: "#ff00ff",
                boxShadow:
                  "0 0 48px 4px rgba(255, 0, 255, 0.8), 0 0 72px 12px rgba(255, 0, 0, 0.7), 0 0 96px 24px rgba(25, 255, 250, 0.5)",
              }}
            />
          </div>

          {/* Description Section */}
          <div className="flex place-items-center text-center text-black col-span-2">
            <p className="text-center xl:text-3xl lg:text-2xl md:text-xl sm:text-lg text-lg font-semibold flex-wrap sm:p-4">
              Neon Studioz is a private, non-government company incorporated on
              April 8, 2022. It is an unlisted company classified as 'company
              limited by shares' with an authorized and fully paid-up capital of
              ₹2.0 lakhs. The company is registered in Mumbai, Maharashtra /
              Indore, Madhya Pradesh and operates under Luminaaz Entertainment
              Private Limited, which has been active in the community, personal,
              and social services sector for over eight years. The current board
              members include Seema Sidhu, and Rikshit Vijay Mata.
            </p>
          </div>
        </div>
      </div>
    </main>
  );
}

export default NeonDescription;
