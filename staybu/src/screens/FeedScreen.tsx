import React, { useState } from "react";
import {
  View,
  Text,
  ScrollView,
  TouchableOpacity,
  StyleSheet,
  TextInput,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { IDEAS, Idea } from "../data/mock";

const TAGS = ["All", "AI", "Fintech", "EdTech", "PropTech", "Sustainability"];

const IdeaCard = ({ idea, onJoin }: { idea: Idea; onJoin: () => void }) => {
  const [liked, setLiked] = useState(false);
  const spots = idea.maxMembers - idea.members;

  return (
    <View style={styles.card}>
      <View style={styles.cardHeader}>
        <View style={styles.avatar}>
          <Text style={styles.avatarText}>{idea.avatar}</Text>
        </View>
        <View style={{ flex: 1 }}>
          <Text style={styles.author}>{idea.author}</Text>
          <Text style={styles.time}>{idea.createdAt}</Text>
        </View>
        <TouchableOpacity onPress={() => setLiked(!liked)} style={styles.likeBtn}>
          <Text style={[styles.likeIcon, liked && { color: "#a855f7" }]}>♥</Text>
          <Text style={styles.likeCount}>{idea.likes + (liked ? 1 : 0)}</Text>
        </TouchableOpacity>
      </View>

      <Text style={styles.ideaTitle}>{idea.title}</Text>
      <Text style={styles.ideaDesc}>{idea.description}</Text>

      <View style={styles.tags}>
        {idea.tags.map((t) => (
          <View key={t} style={styles.tag}>
            <Text style={styles.tagText}>{t}</Text>
          </View>
        ))}
      </View>

      <View style={styles.cardFooter}>
        <View>
          <Text style={styles.skillsLabel}>Looking for</Text>
          <Text style={styles.skills}>{idea.skills.join(" · ")}</Text>
        </View>
        <TouchableOpacity
          style={[styles.joinBtn, spots === 0 && styles.joinBtnFull]}
          onPress={onJoin}
          disabled={spots === 0}
        >
          <Text style={styles.joinBtnText}>
            {spots === 0 ? "Full" : `Join · ${spots} spot${spots > 1 ? "s" : ""}`}
          </Text>
        </TouchableOpacity>
      </View>
    </View>
  );
};

export default function FeedScreen() {
  const [search, setSearch] = useState("");
  const [activeTag, setActiveTag] = useState("All");
  const [joined, setJoined] = useState<string[]>([]);

  const filtered = IDEAS.filter((i) => {
    const matchTag = activeTag === "All" || i.tags.includes(activeTag);
    const matchSearch =
      i.title.toLowerCase().includes(search.toLowerCase()) ||
      i.description.toLowerCase().includes(search.toLowerCase());
    return matchTag && matchSearch;
  });

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.logo}>Staybu</Text>
        <Text style={styles.tagline}>Build together</Text>
      </View>

      <View style={styles.searchBar}>
        <Text style={styles.searchIcon}>🔍</Text>
        <TextInput
          style={styles.searchInput}
          placeholder="Search ideas..."
          placeholderTextColor="#666"
          value={search}
          onChangeText={setSearch}
        />
      </View>

      <ScrollView horizontal showsHorizontalScrollIndicator={false} style={styles.filterBar}>
        {TAGS.map((t) => (
          <TouchableOpacity
            key={t}
            onPress={() => setActiveTag(t)}
            style={[styles.filterChip, activeTag === t && styles.filterChipActive]}
          >
            <Text style={[styles.filterChipText, activeTag === t && styles.filterChipTextActive]}>
              {t}
            </Text>
          </TouchableOpacity>
        ))}
      </ScrollView>

      <ScrollView style={styles.feed} showsVerticalScrollIndicator={false}>
        {filtered.map((idea) => (
          <IdeaCard
            key={idea.id}
            idea={idea}
            onJoin={() => setJoined((prev) => [...prev, idea.id])}
          />
        ))}
        <View style={{ height: 100 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f1a" },
  header: { paddingHorizontal: 20, paddingTop: 8, paddingBottom: 4 },
  logo: { fontSize: 26, fontWeight: "800", color: "#fff" },
  tagline: { fontSize: 13, color: "#a855f7", marginTop: 1 },
  searchBar: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#1a1a2e",
    marginHorizontal: 16,
    marginVertical: 12,
    borderRadius: 12,
    paddingHorizontal: 12,
  },
  searchIcon: { fontSize: 14, marginRight: 8 },
  searchInput: { flex: 1, color: "#fff", fontSize: 15, paddingVertical: 10 },
  filterBar: { paddingLeft: 16, marginBottom: 8, flexGrow: 0 },
  filterChip: {
    paddingHorizontal: 14,
    paddingVertical: 6,
    borderRadius: 20,
    backgroundColor: "#1a1a2e",
    marginRight: 8,
    borderWidth: 1,
    borderColor: "#ffffff15",
  },
  filterChipActive: { backgroundColor: "#7c3aed", borderColor: "#7c3aed" },
  filterChipText: { color: "#888", fontSize: 13 },
  filterChipTextActive: { color: "#fff", fontWeight: "600" },
  feed: { flex: 1, paddingHorizontal: 16 },
  card: {
    backgroundColor: "#1a1a2e",
    borderRadius: 16,
    padding: 16,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: "#ffffff10",
  },
  cardHeader: { flexDirection: "row", alignItems: "center", marginBottom: 12 },
  avatar: {
    width: 38,
    height: 38,
    borderRadius: 19,
    backgroundColor: "#7c3aed",
    alignItems: "center",
    justifyContent: "center",
    marginRight: 10,
  },
  avatarText: { color: "#fff", fontWeight: "700", fontSize: 12 },
  author: { color: "#fff", fontWeight: "600", fontSize: 14 },
  time: { color: "#666", fontSize: 12 },
  likeBtn: { alignItems: "center" },
  likeIcon: { fontSize: 18, color: "#444" },
  likeCount: { color: "#666", fontSize: 11, marginTop: 2 },
  ideaTitle: { color: "#fff", fontSize: 17, fontWeight: "700", marginBottom: 6 },
  ideaDesc: { color: "#aaa", fontSize: 14, lineHeight: 20, marginBottom: 12 },
  tags: { flexDirection: "row", flexWrap: "wrap", gap: 6, marginBottom: 14 },
  tag: {
    backgroundColor: "#7c3aed20",
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderWidth: 1,
    borderColor: "#7c3aed40",
  },
  tagText: { color: "#a855f7", fontSize: 12 },
  cardFooter: { flexDirection: "row", justifyContent: "space-between", alignItems: "flex-end" },
  skillsLabel: { color: "#666", fontSize: 11, marginBottom: 2 },
  skills: { color: "#ccc", fontSize: 13 },
  joinBtn: {
    backgroundColor: "#7c3aed",
    paddingHorizontal: 16,
    paddingVertical: 8,
    borderRadius: 10,
  },
  joinBtnFull: { backgroundColor: "#333" },
  joinBtnText: { color: "#fff", fontWeight: "700", fontSize: 13 },
});
