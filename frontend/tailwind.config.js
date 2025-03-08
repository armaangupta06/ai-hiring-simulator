module.exports = {
    content: ["./src/**/*.{ts,tsx}"],
    darkMode: "class",
    theme: {
      extend: {
        animation: {
          first: "moveVertical 30s ease infinite",
          second: "moveInCircle 20s reverse infinite",
          third: "moveInCircle2 40s linear infinite",
          fourth: "moveHorizontal 40s ease infinite",
          fifth: "moveInCircle3 20s ease infinite",
          "gradient-slow": "gradient 8s ease infinite",
          "gradient-slow-reverse": "gradient 8s ease infinite reverse",
          "shimmer": "shimmer 3s ease-in-out infinite",
        },
        keyframes: {
          gradient: {
            "0%": { backgroundPosition: "0% 50%" },
            "50%": { backgroundPosition: "100% 50%" },
            "100%": { backgroundPosition: "0% 50%" },
          },
          shimmer: {
            "0%": { opacity: 0.1 },
            "50%": { opacity: 0.3 },
            "100%": { opacity: 0.1 },
          },
          moveHorizontal: {
            "0%": {
              transform: "translateX(-200px) translateY(-50px)",
            },
            "25%": {
              transform: "translateX(100px) translateY(100px)",
            },
            "50%": {
              transform: "translateX(200px) translateY(50px)",
            },
            "75%": {
              transform: "translateX(100px) translateY(-100px)",
            },
            "100%": {
              transform: "translateX(-200px) translateY(-50px)",
            },
          },
          moveInCircle: {
            "0%": {
              transform: "rotate(0deg) translate(0, 0)",
            },
            "25%": {
              transform: "rotate(90deg) translate(100px, 100px)",
            },
            "50%": {
              transform: "rotate(180deg) translate(200px, 0)",
            },
            "75%": {
              transform: "rotate(270deg) translate(100px, -100px)",
            },
            "100%": {
              transform: "rotate(360deg) translate(0, 0)",
            },
          },
          moveInCircle2: {
            "0%": {
              transform: "rotate(0deg) translate(0, 0)",
            },
            "25%": {
              transform: "rotate(-90deg) translate(-100px, 100px)",
            },
            "50%": {
              transform: "rotate(-180deg) translate(-200px, 0)",
            },
            "75%": {
              transform: "rotate(-270deg) translate(-100px, -100px)",
            },
            "100%": {
              transform: "rotate(-360deg) translate(0, 0)",
            },
          },
          moveInCircle3: {
            "0%": {
              transform: "rotate(0deg) translate(0, 0)",
            },
            "25%": {
              transform: "rotate(90deg) translate(-100px, -100px)",
            },
            "50%": {
              transform: "rotate(180deg) translate(-200px, 0)",
            },
            "75%": {
              transform: "rotate(270deg) translate(-100px, 100px)",
            },
            "100%": {
              transform: "rotate(360deg) translate(0, 0)",
            },
          },
          moveVertical: {
            "0%": {
              transform: "translateY(-150px) translateX(100px)",
            },
            "25%": {
              transform: "translateY(-75px) translateX(-200px)",
            },
            "50%": {
              transform: "translateY(150px) translateX(100px)",
            },
            "75%": {
              transform: "translateY(75px) translateX(300px)",
            },
            "100%": {
              transform: "translateY(-150px) translateX(100px)",
            },
          },
        },
      },
    },
    plugins: [],
  };
  