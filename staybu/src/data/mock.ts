export type Idea = {
  id: string;
  title: string;
  description: string;
  author: string;
  avatar: string;
  skills: string[];
  members: number;
  maxMembers: number;
  tags: string[];
  likes: number;
  createdAt: string;
};

export type Group = {
  id: string;
  name: string;
  idea: string;
  members: Member[];
  stage: string;
};

export type Member = {
  id: string;
  name: string;
  avatar: string;
  skill: string;
};

export const IDEAS: Idea[] = [
  {
    id: "1",
    title: "AI-powered rent negotiation tool",
    description: "Help renters negotiate better prices using market data and AI scripts.",
    author: "Priya K.",
    avatar: "PK",
    skills: ["Developer", "Marketer"],
    members: 1,
    maxMembers: 3,
    tags: ["PropTech", "AI", "Fintech"],
    likes: 34,
    createdAt: "2h ago",
  },
  {
    id: "2",
    title: "Local food waste marketplace",
    description: "Connect restaurants with surplus food to people who want it at a discount.",
    author: "Marcus T.",
    avatar: "MT",
    skills: ["Designer", "Developer"],
    members: 2,
    maxMembers: 4,
    tags: ["Sustainability", "FoodTech"],
    likes: 58,
    createdAt: "5h ago",
  },
  {
    id: "3",
    title: "Freelancer health insurance pool",
    description: "Group health plans for solo freelancers — strength in numbers.",
    author: "Ana R.",
    avatar: "AR",
    skills: ["Legal", "Marketer", "Developer"],
    members: 1,
    maxMembers: 4,
    tags: ["Insurtech", "Freelance"],
    likes: 91,
    createdAt: "1d ago",
  },
  {
    id: "4",
    title: "Micro-learning for trades workers",
    description: "5-minute daily skill videos for electricians, plumbers, and HVAC techs.",
    author: "Devon S.",
    avatar: "DS",
    skills: ["Content Creator", "Developer"],
    members: 2,
    maxMembers: 3,
    tags: ["EdTech", "Trades"],
    likes: 45,
    createdAt: "2d ago",
  },
];

export const MY_GROUPS: Group[] = [
  {
    id: "1",
    name: "RentAI",
    idea: "AI-powered rent negotiation tool",
    stage: "Validating",
    members: [
      { id: "1", name: "You", avatar: "YO", skill: "Analyst" },
      { id: "2", name: "Priya K.", avatar: "PK", skill: "Developer" },
    ],
  },
];
