export interface NavItem {
  label: string;
  href: string;
  description?: string;
}

export interface NavGroup extends NavItem {
  children?: NavItem[];
}

export const resourceItems: NavItem[] = [
  {
    label: "Student Research",
    href: "/student-research/",
    description: "Future thesis and student research catalog.",
  },
  {
    label: "Research Tools",
    href: "/tools/",
    description: "Future GitHub and browser-accessible tools catalog.",
  },
  {
    label: "Data",
    href: "/data/",
    description: "Future selected dataset and metadata portal.",
  },
  {
    label: "Spatial Explorer",
    href: "/explorer/",
    description: "Future interactive geospatial dashboard.",
  },
  {
    label: "Training",
    href: "/training/",
    description: "Future teaching and training resources.",
  },
];

export const mainNavigation: NavGroup[] = [
  { label: "Research", href: "/research/" },
  { label: "Projects", href: "/projects/" },
  { label: "People", href: "/people/" },
  { label: "Publications", href: "/publications/" },
  {
    label: "Resources",
    href: "/resources/",
    children: resourceItems,
  },
  { label: "About", href: "/about/" },
];

export const footerNavigation = [
  {
    label: "Explore",
    items: mainNavigation.filter((item) =>
      ["Research", "Projects", "People", "Publications"].includes(item.label),
    ),
  },
  {
    label: "Resources",
    items: resourceItems,
  },
  {
    label: "Laboratory",
    items: [{ label: "About", href: "/about/" }],
  },
];

export function normalizePath(pathname: string) {
  if (!pathname || pathname === "/") {
    return "/";
  }

  return pathname.endsWith("/") ? pathname : `${pathname}/`;
}

export function isActivePath(pathname: string, href: string) {
  const currentPath = normalizePath(pathname);
  const targetPath = normalizePath(href);

  if (targetPath === "/") {
    return currentPath === "/";
  }

  return currentPath === targetPath || currentPath.startsWith(targetPath);
}

export function isActiveNavItem(pathname: string, item: NavGroup | NavItem) {
  return (
    isActivePath(pathname, item.href) ||
    ("children" in item &&
      item.children?.some((child) => isActivePath(pathname, child.href)) ===
        true)
  );
}
