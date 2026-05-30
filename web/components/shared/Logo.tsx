export function Logo({ size = "md" }: { size?: "sm" | "md" | "lg" }) {
  const sizes = {
    sm: { icon: 28, text: "text-lg" },
    md: { icon: 32, text: "text-xl" },
    lg: { icon: 48, text: "text-3xl" },
  };
  const { icon, text } = sizes[size];

  return (
    <div className="flex items-center gap-2.5">
      {/* Logo Icon */}
      <svg width={icon} height={icon} viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">
        {/* Background circle */}
        <circle cx="24" cy="24" r="22" fill="#f5f0e8" stroke="#e0d5c0" strokeWidth="2" />

        {/* Indonesia archipelago simplified */}
        <g transform="translate(8, 12)">
          {/* Sumatera */}
          <ellipse cx="8" cy="10" rx="4" ry="7" fill="#c4703f" opacity="0.8" />
          {/* Jawa */}
          <ellipse cx="16" cy="14" rx="5" ry="2.5" fill="#c4703f" opacity="0.9" />
          {/* Kalimantan */}
          <ellipse cx="16" cy="6" rx="5" ry="5" fill="#c4703f" opacity="0.7" />
          {/* Sulawesi */}
          <path d="M22 4 C24 4, 26 8, 24 12 C22 16, 26 18, 24 20" stroke="#8b3a3a" strokeWidth="2" fill="none" strokeLinecap="round" />
          {/* Papua */}
          <ellipse cx="28" cy="10" rx="3" ry="4" fill="#5a7247" opacity="0.8" />
          {/* Bali/NTB */}
          <circle cx="22" cy="15" r="1.5" fill="#c4703f" opacity="0.7" />
        </g>

        {/* Speech bubble accent */}
        <circle cx="36" cy="36" r="8" fill="#c4703f" />
        <text x="36" y="40" textAnchor="middle" fill="white" fontSize="10" fontWeight="bold">Aa</text>
      </svg>

      {/* Text */}
      <div className="leading-tight">
        <span className={`font-bold text-earth-700 ${text}`}>Nusantara</span>
        <span className={`font-light text-earth-600 ${text}`}>Basa</span>
      </div>
    </div>
  );
}
