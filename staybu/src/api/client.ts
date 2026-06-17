import AsyncStorage from "@react-native-async-storage/async-storage";

const BASE_URL = "https://styabu-server-production.up.railway.app";

async function getToken() {
  return AsyncStorage.getItem("token");
}

async function request(path: string, options: RequestInit = {}) {
  const token = await getToken();
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    },
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || "Request failed");
  return data;
}

export const api = {
  // Auth
  register: (name: string, email: string, password: string) =>
    request("/auth/register", { method: "POST", body: JSON.stringify({ name, email, password }) }),

  login: (email: string, password: string) =>
    request("/auth/login", { method: "POST", body: JSON.stringify({ email, password }) }),

  // Ideas
  getIdeas: (search?: string, tag?: string) => {
    const params = new URLSearchParams();
    if (search) params.append("search", search);
    if (tag && tag !== "All") params.append("tag", tag);
    return request(`/ideas?${params}`);
  },

  postIdea: (data: { title: string; description: string; skills_needed: string[]; tags: string[]; max_members: number }) =>
    request("/ideas", { method: "POST", body: JSON.stringify(data) }),

  likeIdea: (id: number) =>
    request(`/ideas/${id}/like`, { method: "POST" }),

  requestJoin: (ideaId: number, message: string) =>
    request(`/ideas/${ideaId}/request`, { method: "POST", body: JSON.stringify({ message }) }),

  getJoinRequests: (ideaId: number) =>
    request(`/ideas/${ideaId}/requests`),

  approveRequest: (requestId: number) =>
    request(`/requests/${requestId}/approve`, { method: "POST" }),

  // Groups
  getMyGroups: () => request("/groups/mine"),

  updateStage: (groupId: number, stage: string) =>
    request(`/groups/${groupId}/stage`, { method: "PATCH", body: JSON.stringify({ stage }) }),

  // Profile
  getProfile: () => request("/profile"),

  updateProfile: (data: { name: string; skills: string[]; availability: string; location: string }) =>
    request("/profile", { method: "PATCH", body: JSON.stringify(data) }),
};
