import { NavLink } from "react-router-dom";

const navigationItems = [
  { label: "Portfolio", path: "/welcome", icon: "◈" },
  { label: "Risk Center", path: "/risk-center", icon: "◉" },
  { label: "Predictions", path: "/prediction", icon: "◇" },
  { label: "Projects", path: "/projects", icon: "▣" },
  { label: "Early Warning", path: "/early-warning", icon: "△" },
  { label: "Investigation", path: "/investigation", icon: "⌁" },
  { label: "Scenarios", path: "/scenario-simulation", icon: "↗" },
  { label: "Reports", path: "/project-report", icon: "▤" },
];

function SideRail() {
  return (
    <aside className="aurex-side-rail">
      <div className="aurex-brand">
        <div className="aurex-brand-mark">A</div>

        <div>
          <div className="aurex-brand-name">AUREX</div>
          <div className="aurex-brand-subtitle">INTELLIGENCE</div>
        </div>
      </div>

      <nav className="aurex-navigation">
        {navigationItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `aurex-nav-item ${isActive ? "active" : ""}`
            }
          >
            <span className="aurex-nav-icon">{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="aurex-system-status">
        <span className="aurex-status-dot" />
        <div>
          <div className="aurex-status-label">SYSTEM</div>
          <div className="aurex-status-value">OPERATIONAL</div>
        </div>
      </div>
    </aside>
  );
}

export default SideRail;