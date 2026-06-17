import React, { useState } from "react";
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet,
  Modal, TextInput, Alert, ActivityIndicator,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

type Idea = {
  id: number;
  title: string;
  description: string;
  author_name: string;
  author_id: number;
  skills_needed: string[];
  tags: string[];
  max_members: number;
  member_count: number;
  likes: number;
  created_at: string;
};

export default function IdeaDetailScreen({ route, navigation }: any) {
  const { idea }: { idea: Idea } = route.params;
  const { user } = useAuth();

  const [liked, setLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(idea.likes || 0);
  const [showJoinModal, setShowJoinModal] = useState(false);
  const [joinMessage, setJoinMessage] = useState("");
  const [submitting, setSubmitting] = useState(false);

  const isAuthor = user?.id === idea.author_id;
  const spots = idea.max_members - (idea.member_count || 0);
  const initials = idea.author_name?.split(" ").map((n: string) => n[0]).join("").toUpperCase().slice(0, 2) || "?";

  const timeAgo = (dateStr: string) => {
    const diff = Date.now() - new Date(dateStr).getTime();
    const h = Math.floor(diff / 3600000);
    if (h < 1) return "just now";
    if (h < 24) return `${h}h ago`;
    return `${Math.floor(h / 24)}d ago`;
  };

  const handleLike = async () => {
    if (liked) return;
    setLiked(true);
    setLikeCount((c) => c + 1);
    try {
      await api.likeIdea(idea.id);
    } catch {
      setLiked(false);
      setLikeCount((c) => c - 1);
    }
  };

  const handleJoinSubmit = async () => {
    setSubmitting(true);
    try {
      await api.requestJoin(idea.id, joinMessage);
      setShowJoinModal(false);
      setJoinMessage("");
      Alert.alert("Request sent!", `Your request to join "${idea.title}" has been sent.`);
    } catch (e: any) {
      Alert.alert("Error", e.message);
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.topBar}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <Text style={styles.backBtnText}>← Back</Text>
        </TouchableOpacity>
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Author */}
        <View style={styles.authorRow}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>{initials}</Text>
          </View>
          <View>
            <Text style={styles.authorName}>{idea.author_name}</Text>
            <Text style={styles.timeText}>{timeAgo(idea.created_at)}</Text>
          </View>
        </View>

        {/* Title & Description */}
        <View style={styles.content}>
          <Text style={styles.title}>{idea.title}</Text>
          <Text style={styles.description}>{idea.description}</Text>
        </View>

        {/* Tags */}
        {idea.tags && idea.tags.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionLabel}>Tags</Text>
            <View style={styles.tagRow}>
              {idea.tags.map((t) => (
                <View key={t} style={styles.tag}>
                  <Text style={styles.tagText}>{t}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {/* Skills needed */}
        {idea.skills_needed && idea.skills_needed.length > 0 && (
          <View style={styles.section}>
            <Text style={styles.sectionLabel}>Looking for</Text>
            <View style={styles.tagRow}>
              {idea.skills_needed.map((s) => (
                <View key={s} style={styles.skillTag}>
                  <Text style={styles.skillTagText}>{s}</Text>
                </View>
              ))}
            </View>
          </View>
        )}

        {/* Stats */}
        <View style={styles.statsRow}>
          <View style={styles.statItem}>
            <Text style={styles.statNum}>{idea.member_count || 0}</Text>
            <Text style={styles.statLabel}>Members</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statNum}>{spots > 0 ? spots : 0}</Text>
            <Text style={styles.statLabel}>Spots left</Text>
          </View>
          <View style={styles.statDivider} />
          <View style={styles.statItem}>
            <Text style={styles.statNum}>{likeCount}</Text>
            <Text style={styles.statLabel}>Likes</Text>
          </View>
        </View>

        {/* Actions */}
        <View style={styles.actions}>
          <TouchableOpacity
            style={[styles.likeBtn, liked && styles.likeBtnActive]}
            onPress={handleLike}
          >
            <Text style={[styles.likeBtnText, liked && styles.likeBtnTextActive]}>
              {liked ? "♥ Liked" : "♡ Like"}
            </Text>
          </TouchableOpacity>

          {isAuthor ? (
            <TouchableOpacity
              style={styles.primaryBtn}
              onPress={() => Alert.alert("Manage your group", "Head to the Groups tab to manage join requests and your team.")}
            >
              <Text style={styles.primaryBtnText}>View Requests</Text>
            </TouchableOpacity>
          ) : (
            <TouchableOpacity
              style={[styles.primaryBtn, spots <= 0 && styles.primaryBtnDisabled]}
              onPress={() => spots > 0 && setShowJoinModal(true)}
              disabled={spots <= 0}
            >
              <Text style={styles.primaryBtnText}>
                {spots <= 0 ? "Group Full" : "Request to Join"}
              </Text>
            </TouchableOpacity>
          )}
        </View>

        <View style={{ height: 100 }} />
      </ScrollView>

      {/* Join Request Modal */}
      <Modal
        visible={showJoinModal}
        transparent
        animationType="slide"
        onRequestClose={() => setShowJoinModal(false)}
      >
        <View style={styles.modalOverlay}>
          <View style={styles.modalSheet}>
            <View style={styles.modalHandle} />
            <Text style={styles.modalTitle}>Request to Join</Text>
            <Text style={styles.modalSubtitle}>{idea.title}</Text>

            <Text style={styles.modalLabel}>Why do you want to join? (optional)</Text>
            <TextInput
              style={styles.modalInput}
              value={joinMessage}
              onChangeText={setJoinMessage}
              placeholder="Tell the founder about yourself and why you're excited about this idea..."
              placeholderTextColor="#555"
              multiline
              numberOfLines={4}
              textAlignVertical="top"
            />

            <TouchableOpacity
              style={[styles.submitBtn, submitting && styles.submitBtnDisabled]}
              onPress={handleJoinSubmit}
              disabled={submitting}
            >
              {submitting ? (
                <ActivityIndicator color="#fff" />
              ) : (
                <Text style={styles.submitBtnText}>Send Request</Text>
              )}
            </TouchableOpacity>

            <TouchableOpacity style={styles.cancelBtn} onPress={() => setShowJoinModal(false)}>
              <Text style={styles.cancelBtnText}>Cancel</Text>
            </TouchableOpacity>
          </View>
        </View>
      </Modal>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f1a" },
  topBar: { paddingHorizontal: 16, paddingVertical: 8 },
  backBtn: { padding: 4 },
  backBtnText: { color: "#a855f7", fontSize: 16, fontWeight: "600" },
  authorRow: {
    flexDirection: "row", alignItems: "center", paddingHorizontal: 20,
    paddingBottom: 16, gap: 12,
  },
  avatar: {
    width: 44, height: 44, borderRadius: 22, backgroundColor: "#7c3aed",
    alignItems: "center", justifyContent: "center",
  },
  avatarText: { color: "#fff", fontWeight: "700", fontSize: 14 },
  authorName: { color: "#fff", fontWeight: "700", fontSize: 15 },
  timeText: { color: "#666", fontSize: 12, marginTop: 2 },
  content: { paddingHorizontal: 20, marginBottom: 20 },
  title: { color: "#fff", fontSize: 24, fontWeight: "800", marginBottom: 12, lineHeight: 30 },
  description: { color: "#bbb", fontSize: 15, lineHeight: 24 },
  section: { paddingHorizontal: 20, marginBottom: 20 },
  sectionLabel: { color: "#666", fontSize: 12, fontWeight: "600", marginBottom: 8, textTransform: "uppercase", letterSpacing: 0.5 },
  tagRow: { flexDirection: "row", flexWrap: "wrap", gap: 6 },
  tag: { backgroundColor: "#7c3aed20", borderRadius: 8, paddingHorizontal: 12, paddingVertical: 5, borderWidth: 1, borderColor: "#7c3aed40" },
  tagText: { color: "#a855f7", fontSize: 13 },
  skillTag: { backgroundColor: "#ffffff10", borderRadius: 8, paddingHorizontal: 12, paddingVertical: 5, borderWidth: 1, borderColor: "#ffffff20" },
  skillTagText: { color: "#ddd", fontSize: 13 },
  statsRow: {
    flexDirection: "row", alignItems: "center", marginHorizontal: 20,
    backgroundColor: "#1a1a2e", borderRadius: 16, padding: 20, marginBottom: 24,
    borderWidth: 1, borderColor: "#ffffff10",
  },
  statItem: { flex: 1, alignItems: "center" },
  statNum: { color: "#fff", fontSize: 22, fontWeight: "800" },
  statLabel: { color: "#666", fontSize: 12, marginTop: 2 },
  statDivider: { width: 1, height: 36, backgroundColor: "#ffffff15" },
  actions: { flexDirection: "row", paddingHorizontal: 20, gap: 10, marginBottom: 20 },
  likeBtn: {
    flex: 1, paddingVertical: 12, borderRadius: 12,
    alignItems: "center", borderWidth: 1, borderColor: "#7c3aed", backgroundColor: "transparent",
  },
  likeBtnActive: { backgroundColor: "#7c3aed20" },
  likeBtnText: { color: "#a855f7", fontWeight: "700", fontSize: 15 },
  likeBtnTextActive: { color: "#c084fc" },
  primaryBtn: {
    flex: 2, paddingVertical: 12, borderRadius: 12,
    alignItems: "center", backgroundColor: "#7c3aed",
  },
  primaryBtnDisabled: { backgroundColor: "#333" },
  primaryBtnText: { color: "#fff", fontWeight: "700", fontSize: 15 },
  // Modal
  modalOverlay: {
    flex: 1, backgroundColor: "#000000aa",
    justifyContent: "flex-end",
  },
  modalSheet: {
    backgroundColor: "#1a1a2e", borderTopLeftRadius: 24, borderTopRightRadius: 24,
    padding: 24, paddingBottom: 40,
  },
  modalHandle: {
    width: 36, height: 4, backgroundColor: "#ffffff30", borderRadius: 2,
    alignSelf: "center", marginBottom: 20,
  },
  modalTitle: { color: "#fff", fontSize: 20, fontWeight: "800", marginBottom: 4 },
  modalSubtitle: { color: "#888", fontSize: 14, marginBottom: 20 },
  modalLabel: { color: "#aaa", fontSize: 13, marginBottom: 8 },
  modalInput: {
    backgroundColor: "#0f0f1a", borderRadius: 12, padding: 14, color: "#fff",
    fontSize: 14, borderWidth: 1, borderColor: "#ffffff15", height: 120, marginBottom: 16,
  },
  submitBtn: { backgroundColor: "#7c3aed", borderRadius: 12, paddingVertical: 14, alignItems: "center", marginBottom: 10 },
  submitBtnDisabled: { opacity: 0.6 },
  submitBtnText: { color: "#fff", fontWeight: "700", fontSize: 15 },
  cancelBtn: { alignItems: "center", paddingVertical: 12 },
  cancelBtnText: { color: "#666", fontSize: 15 },
});
