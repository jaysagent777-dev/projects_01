import React, { useCallback, useEffect, useState } from "react";
import {
  View, Text, ScrollView, TouchableOpacity,
  StyleSheet, TextInput, RefreshControl, Alert, ActivityIndicator,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const TAGS = ["All", "AI", "Fintech", "EdTech", "PropTech", "Sustainability", "HealthTech", "SaaS"];

type Idea = {
  id: number;
  title: string;
  description: string;
  author_name: string;
  skills_needed: string[];
  tags: string[];
  max_members: number;
  member_count: number;
  likes: number;
  created_at: string;
};

const IdeaCard = ({ idea, onJoin, onLike, onPress }: { idea: Idea; onJoin: () => void; onLike: () => void; onPress: () => void }) => {
  const [liked, setLiked] = useState(false);
  const spots = idea.max_members - (idea.member_count || 0);
  const initials = idea.author_name.split(" ").map((n) => n[0]).join("").toUpperCase().slice(0, 2);

  const timeAgo = (dateStr: string) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const h = Math.floor(diff / 3600000);
    if (h < 1) return "just now";
    if (h < 24) return `${h}h ago`;
    return `${Math.floor(h / 24)}d ago`;
  };

  const handleLike = () => {
    setLiked(!liked);
    onLike();
  };

  return (
    <TouchableOpacity style={styles.card} onPress={onPress} activeOpacity={0.9}>
      <View style={styles.cardHeader}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>{initials}</Text>
        </View>
        <View style={{ flex: 1 }}>
          <Text style={styles.author}>{idea.author_name}</Text>
          <Text style={styles.time}>{timeAgo(idea.created_at)}</Text>
        </View>
        <TouchableOpacity onPress={handleLike} style={styles.likeBtn}>
          <Text style={[styles.likeIcon, liked && { color: "#a855f7" }]}>♥</Text>
          <Text style={styles.likeCount}>{idea.likes + (liked ? 1 : 0)}</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.ideaTitle}>{idea.title}</Text>
      <Text style={styles.ideaDesc}>{idea.description}</Text>

      {idea.tags.length > 0 && (
        <View style={styles.tags}>
          {idea.tags.map((t) => (
            <View key={t} style={styles.tag}>
              <Text style={styles.tagText}>{t}</Text>
            </View>
          ))}
        </View>
      )}

      <View style={styles.cardFooter}>
        <View>
          {idea.skills_needed.length > 0 && (
            <>
              <Text style={styles.skillsLabel}>Looking for</Text>
              <Text style={styles.skills}>{idea.skills_needed.join(" · ")}</Text>
            </>
          )}
        </View>
        <TouchableOpacity
          style={[styles.joinBtn, spots <= 0 && styles.joinBtnFull]}
          onPress={onJoin}
          disabled={spots <= 0}
        >
          <Text style={styles.joinBtnText}>
            {spots <= 0 ? "Full" : `Join · ${spots} spot${spots > 1 ? "s" : ""}`}
          </Text>
        </TouchableOpacity>
      </View>
    </TouchableOpacity>
  );
};

export default function FeedScreen({ navigation }: any) {
  const { user } = useAuth();
  const [ideas, setIdeas] = useState<Idea[]>([]);
  const [search, setSearch] = useState("");
  const [activeTag, setActiveTag] = useState("All");
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [showPost, setShowPost] = useState(false);
  const [newTitle, setNewTitle] = useState("");
  const [newDesc, setNewDesc] = useState("");
  const [newTags, setNewTags] = useState("");
  const [newSkills, setNewSkills] = useState("");

  const fetchIdeas = useCallback(async () => {
    try {
      const data = await api.getIdeas(search);
      setIdeas(data);
    } catch (e: any) {
      Alert.alert("Error", e.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [search]);

  useEffect(() => {
    fetchIdeas();
  }, [fetchIdeas]);

  const handleJoin = async (idea: Idea) => {
    try {
      await api.requestJoin(idea.id, "");
      Alert.alert("Request sent!", `You've requested to join "${idea.title}"`);
    } catch (e: any) {
      Alert.alert("Error", e.message);
    }
  };

  const handlePostIdea = async () => {
    if (!newTitle || !newDesc) return Alert.alert("Fill in title and description");
    try {
      await api.postIdea({
        title: newTitle,
        description: newDesc,
        tags: newTags.split(",").map((t) => t.trim()).filter(Boolean),
        skills_needed: newSkills.split(",").map((s) => s.trim()).filter(Boolean),
        max_members: 4,
      });
      setShowPost(false);
      setNewTitle(""); setNewDesc(""); setNewTags(""); setNewSkills("");
      fetchIdeas();
    } catch (e: any) {
      Alert.alert("Error", e.message);
    }
  };

  const filtered = activeTag === "All"
    ? ideas
    : ideas.filter((i) => i.tags.includes(activeTag));

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <View>
          <Text style={styles.logo}>Styabu</Text>
          <Text style={styles.tagline}>Build together</Text>
        </View>
        <TouchableOpacity style={styles.postBtn} onPress={() => setShowPost(!showPost)}>
          <Text style={styles.postBtnText}>{showPost ? "✕" : "+ Idea"}</Text>
        </TouchableOpacity>
      </View>

      {showPost && (
        <View style={styles.postForm}>
          <TextInput style={styles.postInput} placeholder="Idea title" placeholderTextColor="#555" value={newTitle} onChangeText={setNewTitle} />
          <TextInput style={[styles.postInput, { height: 80 }]} placeholder="Describe the problem you're solving..." placeholderTextColor="#555" value={newDesc} onChangeText={setNewDesc} multiline />
          <TextInput style={styles.postInput} placeholder="Tags (comma separated: AI, Fintech)" placeholderTextColor="#555" value={newTags} onChangeText={setNewTags} />
          <TextInput style={styles.postInput} placeholder="Skills needed (Developer, Designer)" placeholderTextColor="#555" value={newSkills} onChangeText={setNewSkills} />
          <TouchableOpacity style={styles.submitBtn} onPress={handlePostIdea}>
            <Text style={styles.submitBtnText}>Post Idea</Text>
          </TouchableOpacity>
        </View>
      )}

      <View style={styles.searchBar}>
        <Text style={styles.searchIcon}>🔍</Text>
        <TextInput
          style={styles.searchInput}
          placeholder="Search ideas..."
          placeholderTextColor="#555"
          value={search}
          onChangeText={setSearch}
        />
      </View>

      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterBar}>
        {TAGS.map((t) => (
          <TouchableOpacity key={t} onPress={() => setActiveTag(t)} style={[styles.filterChip, activeTag === t && styles.filterChipActive]}>
            <Text style={[styles.filterChipText, activeTag === t && styles.filterChipTextActive]}>{t}</Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      {loading ? (
        <ActivityIndicator color="#7c3aed" style={{ marginTop: 40 }} />
      ) : (
        <ScrollView
          style={styles.feed}
          showsVerticalScrollIndicator={false}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={() => { setRefreshing(true); fetchIdeas(); }} tintColor="#7c3aed" />}
        >
          {filtered.length === 0 ? (
            <View style={styles.empty}>
              <Text style={styles.emptyIcon}>💡</Text>
              <Text style={styles.emptyTitle}>No ideas yet</Text>
              <Text style={styles.emptyText}>Be the first to post one</Text>
            </View>
          ) : (
            filtered.map((idea) => (
              <IdeaCard
                key={idea.id}
                idea={idea}
                onJoin={() => handleJoin(idea)}
                onLike={() => api.likeIdea(idea.id)}
                onPress={() => navigation.navigate("IdeaDetail", { idea })}
              />
            ))
          )}
          <View style={{ height: 100 }} />
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f1a" },
  header: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", paddingHorizontal: 20, paddingTop: 8, paddingBottom: 4 },
  logo: { fontSize: 26, fontWeight: "800", color: "#fff" },
  tagline: { fontSize: 13, color: "#a855f7", marginTop: 1 },
  postBtn: { backgroundColor: "#7c3aed", paddingHorizontal: 14, paddingVertical: 8, borderRadius: 10 },
  postBtnText: { color: "#fff", fontWeight: "700", fontSize: 13 },
  postForm: { backgroundColor: "#1a1a2e", margin: 16, borderRadius: 16, padding: 14, gap: 10, borderWidth: 1, borderColor: "#7c3aed40" },
  postInput: { backgroundColor: "#0f0f1a", borderRadius: 10, padding: 12, color: "#fff", fontSize: 14, borderWidth: 1, borderColor: "#ffffff10" },
  submitBtn: { backgroundColor: "#7c3aed", borderRadius: 10, padding: 12, alignItems: "center" },
  submitBtnText: { color: "#fff", fontWeight: "700" },
  searchBar: { flexDirection: "row", alignItems: "center", backgroundColor: "#1a1a2e", marginHorizontal: 16, marginVertical: 10, borderRadius: 12, paddingHorizontal: 12 },
  searchIcon: { fontSize: 14, marginRight: 8 },
  searchInput: { flex: 1, color: "#fff", fontSize: 15, paddingVertical: 10 },
  filterBar: { paddingLeft: 16, marginBottom: 8, flexGrow: 0 },
  filterChip: { paddingHorizontal: 14, paddingVertical: 6, borderRadius: 20, backgroundColor: "#1a1a2e", marginRight: 8, borderWidth: 1, borderColor: "#ffffff15" },
  filterChipActive: { backgroundColor: "#7c3aed", borderColor: "#7c3aed" },
  filterChipText: { color: "#888", fontSize: 13 },
  filterChipTextActive: { color: "#fff", fontWeight: "600" },
  feed: { flex: 1, paddingHorizontal: 16 },
  card: { backgroundColor: "#1a1a2e", borderRadius: 16, padding: 16, marginBottom: 14, borderWidth: 1, borderColor: "#ffffff10" },
  cardHeader: { flexDirection: "row", alignItems: "center", marginBottom: 12 },
  avatar: { width: 38, height: 38, borderRadius: 19, backgroundColor: "#7c3aed", alignItems: "center", justifyContent: "center", marginRight: 10 },
  avatarText: { color: "#fff", fontWeight: "700", fontSize: 12 },
  author: { color: "#fff", fontWeight: "600", fontSize: 14 },
  time: { color: "#666", fontSize: 12 },
  likeBtn: { alignItems: "center" },
  likeIcon: { fontSize: 18, color: "#444" },
  likeCount: { color: "#666", fontSize: 11, marginTop: 2 },
  ideaTitle: { color: "#fff", fontSize: 17, fontWeight: "700", marginBottom: 6 },
  ideaDesc: { color: "#aaa", fontSize: 14, lineHeight: 20, marginBottom: 12 },
  tags: { flexDirection: "row", flexWrap: "wrap", gap: 6, marginBottom: 14 },
  tag: { backgroundColor: "#7c3aed20", borderRadius: 8, paddingHorizontal: 10, paddingVertical: 4, borderWidth: 1, borderColor: "#7c3aed40" },
  tagText: { color: "#a855f7", fontSize: 12 },
  cardFooter: { flexDirection: "row", justifyContent: "space-between", alignItems: "flex-end" },
  skillsLabel: { color: "#666", fontSize: 11, marginBottom: 2 },
  skills: { color: "#ccc", fontSize: 13 },
  joinBtn: { backgroundColor: "#7c3aed", paddingHorizontal: 16, paddingVertical: 8, borderRadius: 10 },
  joinBtnFull: { backgroundColor: "#333" },
  joinBtnText: { color: "#fff", fontWeight: "700", fontSize: 13 },
  empty: { alignItems: "center", paddingTop: 80 },
  emptyIcon: { fontSize: 48, marginBottom: 12 },
  emptyTitle: { color: "#fff", fontSize: 20, fontWeight: "700", marginBottom: 6 },
  emptyText: { color: "#666", fontSize: 14 },
});
