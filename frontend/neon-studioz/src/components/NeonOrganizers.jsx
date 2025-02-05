import React from "react";

function NeonOrganizers() {
  return (
    <div className="flex flex-col items-center justify-center w-full min-h-screen px-4 sm:px-6 lg:px-8 gap-8 sm:gap-16">
      {/* Rikshit Matta Section */}

      <div className="flex items-center justify-center w-full min-h-screen px-4 sm:px-6 lg:px-8">
        <div className="grid gap-4 sm:gap-8 w-full max-w-7xl px-4 py-2">
          {/* Title Section */}
          <h2
            className="text-3xl sm:text-4xl md:text-5xl lg:text-7xl font-black text-center text-gray-100 mb-4 sm:mb-8 "
            style={{
              color: "#fcfcfc",
              WebkitTextStroke: "2px #01D41A",
              // textShadow: "0 0 20px #01D41A",
            }}
          >
            THE ORGANIZERS
          </h2>

          {/* Grid Layout for Content */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 sm:gap-8 items-center">
            {/* Image Section */}
            <div className="flex justify-center items-center rounded-2xl h-full p-4 transition duration-300 hover:-rotate-3 hover:scale-105">
              <img
                src="/Rikshit-Seema.jpg" // Ensure the path is correct
                alt="Neon Logo"
                className="w-40 sm:w-56 md:w-72 lg:w-80 aspect-auto rounded-2xl"
              />
            </div>

            {/* Description Section */}
            <div className="flex flex-col col-span-1 md:col-span-2 justify-center items-center text-center text-white">
              <h1 className="text-white font-extrabold text-2xl sm:text-3xl md:text-4xl h-full">
                <div className="flex lg:flex-row flex-col items-center justify-center h-full lg:gap-16 md:gap-12 gap-6 mb-2 pb-4">
                  <div className="flex flex-row items-center justify-center gap-1 h-full ">
                    <p className="flex flex-row h-full justify-start items-start">
                      {"***"}
                    </p>
                    <p className="font-brush-king">RIKSHIT</p>
                  </div>
                  <p className="font-brush-king">MATTA</p>
                </div>
              </h1>
              <p className="text-justify xl:text-3xl lg:text-2xl md:text-xl sm:text-lg text-lg  flex-wrap sm:p-4 py-4 ">
                The man behind the most creative and new concepts with a zeal to
                establish a mark in the field of movies, TV, and now events.
                Rikshit Matta started his career with acting but became a
                successful TV head in channels like Sony, Colors, Zee TV, and
                Star, respectively. Later, he launched his own production house
                and directed ad films, music videos, and two films which are
                ready for release. Presently handling mega events and various
                prestigious projects, he has worked with prominent figures in
                the film industry and media. Rikshit is still quenching his
                thirst to excel in creating novel concepts in events, films, and
                much more, along with his new firm - Rikshit Constructions And
                Co. in Indore.
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Seema Sidhu Section */}
      <div className="flex flex-col justify-center items-center text-center text-white w-full max-w-7xl px-4 sm:px-8">
        <div className="w-full p-2 border-t  border-gray-300  sm:max-w-2xl lg:max-w-4xl xl:max-w-6xl max-w-xs"></div>
        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4 sm:gap-8 my-4 sm:my-12">
          <img
            src="/home/picture1.png"
            alt="picture1"
            className="w-full h-auto rounded-lg p-4 transition duration-300 hover:scale-105 hover:shadow-lg hover:shadow-pink-600"
          />
          <img
            src="/home/picture2.png"
            alt="picture2"
            className="w-full h-auto rounded-lg p-4 transition duration-300 hover:scale-105 hover:shadow-lg hover:shadow-yellow-600"
          />
          <img
            src="/home/picture3.png"
            alt="picture3"
            className="w-full h-auto rounded-lg p-4 transition duration-300 hover:scale-105 hover:shadow-lg hover:shadow-blue-600"
          />
        </div>
        <h1 className="text-white font-extrabold text-2xl sm:text-3xl md:text-4xl font-brush-king pt-12">
          <div className="flex lg:flex-row flex-col items-center justify-center lg:gap-16 md:gap-12 gap-6 mb-2 pb-4">
            <p>SEEMA</p>
            <p>SIDHU</p>
          </div>
        </h1>
        <div className="grid grid-rows-3 w-full md:p-4 sm:py-6 sm:gap-4">
          <div className="xl:text-3xl lg:text-2xl md:text-xl sm:text-lg text-lg  flex items-center justify-center text-center">
            Seema Sidhu is synonymous with fast and efficient production,
            creating new forms of events in terms of music and the Bollywood
            industry.{" "}
          </div>
          <div className="xl:text-3xl lg:text-2xl md:text-xl sm:text-lg text-lg  flex items-center justify-center text-center">
            She started her career with media acting and films, later developing
            into the conceptualization of projects involving advertising,
            promotions, celebrity management, film distribution, commercial
            tie-ups, and media endorsements.
          </div>
          <div className="xl:text-3xl lg:text-2xl md:text-xl sm:text-lg text-lg  flex items-center justify-center text-center">
            Among her commendable achievements, she holds expertise in managing
            the film fraternity, global music industry, and sports industry.
          </div>
        </div>
      </div>
    </div>
  );
}

export default NeonOrganizers;
