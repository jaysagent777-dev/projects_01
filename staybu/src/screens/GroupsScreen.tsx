import React, { useCallback, useEffect, useState } from "react";
import {
  View, Text, ScrollView, TouchableOpacity,
  StyleSheet, RefreshControl, ActivityIndicator, Alert,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const STAGES = ["Idea", "Validating", "Building", "Launched"];

type Member = {
  id: number;
  name: string;
  skills: string; // JSON string from server
  role: string;
};

type Group = {
  id: number;
  idea_id: number;
  idea_title: string;
  idea_description: string;
  stage: string;
  members: Member[];
  pending_requests?: number;
};

export default function GroupsScreen({ navigation }: any) {
  const { user } = useAuth();
  const [groups, setGroups] = useState<Group[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [pendingCounts, setPendingCounts] = useState<Record<number, number>>({});

  const fetchGroups = useCallback(async () => {
    try {
      const data = await api.getMyGroups();
      setGroups(data);

      // Fetch pending request counts for groups where current user is owner
      const owned = data.filter((g: Group) =>
        g.members?.some((m: Member) => m.id === user?.id && m.role === "owner")
      );
      const counts: Record<number, number> = {};
      await Promise.all(
        owned.map(async (g: Group) => {
          try {
            const reqs = await api.getJoinRequests(g.idea_id);
            const pending = reqs.filter((r: any) => r.status === "pending");
            if (pending.length > 0) counts[g.id] = pending.length;
          } catch {}
        })
      );
      setPendingCounts(counts);
    } catch (e: any) {
      Alert.alert("Error", e.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [user?.id]);

  useEffect(() => {
    fetchGroups();
  }, [fetchGroups]);

  const onRefresh = () => {
    setRefreshing(true);
    fetchGroups();
  };

  const getInitials = (name: string) =>
    name.split(" ").map((n) => n[0]).join("").toUpperCase().slice(0, 2);

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>My Groups</Text>
      </View>

      {loading ? (
        <ActivityIndicator color="#7c3aed" style={{ marginTop: 60 }} />
      ) : (
        <ScrollView
          style={styles.scroll}
          showsVerticalScrollIndicator={false}
          refreshControl={
            <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor="#7c3aed" />
          }
        >
          {groups.length === 0 ? (
            <View style={styles.empty}>
              <Text style={styles.emptyIcon}>🚀</Text>
              <Text style={styles.emptyTitle}>No groups yet</Text>
              <Text style={styles.emptyText}>Post an idea or join one from the feed</Text>
            </View>
          ) : (
            groups.map((group) => {
              const stageIndex = STAGES.indexOf(group.stage);
              const pending = pendingCounts[group.id] || 0;

              return (
                <TouchableOpacity
                  key={group.id}
                  style={styles.card}
                  onPress={() => {
                    const ownerMember = group.members?.find((m: Member) => m.role === "owner");
                    navigation.navigate("GroupDetail", {
                      group: { ...group, owner_id: ownerMember?.id },
                      onRefresh: fetchGroups,
                    });
                  }}
                  activeOpacity={0.85}
                >
                  <View style={styles.cardTop}>
                    <Text style={styles.groupName} numberOfLines={1}>{group.idea_title}</Text>
                    <View style={styles.stageBadge}>
                      <Text style={styles.stageText}>{group.stage}</Text>
                    </View>
                  </View>

                  {group.idea_description ? (
                    <Text style={styles.ideaText} numberOfLines={2}>{group.idea_description}</Text>
                  ) : null}

                  {/* Stage progress bar */}
                  <View style={styles.stageBar}>
                    {STAGES.map((s, i) => (
                      <View key={s} style={styles.stageStep}>
                        <View style={[styles.stageDot, stageIndex >= i && styles.stageDotActive]} />
                        <Text style={[styles.stageLabel, stageIndex >= i && styles.stageLabelActive]}>{s}</Text>
                      </View>
                    ))}
                    <View style={styles.stageConnector}>
                      <View style={[styles.stageConnectorFill, { width: `${(stageIndex / (STAGES.length - 1)) * 100}%` }]} />
                    </View>
                  </View>

                  {/* Members */}
                  {group.members && group.members.length > 0 && (
                    <View style={styles.members}>
                      <Text style={styles.membersLabel}>Team</Text>
                      <ScrollView horizontal showsHorizontalScrollIndicator={false}>
                        <View style={styles.memberRow}>
                          {group.members.map((m) => (
                            <View key={m.id} style={styles.memberChip}>
                              <View style={[styles.memberAvatar, m.role === "owner" && styles.memberAvatarOwner]}>
                                <Text style={styles.memberAvatarText}>{getInitials(m.name)}</Text>
                              </View>
                              <View>
                                <View style={{ flexDirection: "row", alignItems: "center", gap: 4 }}>
                                  <Text style={styles.memberName}>{m.name}</Text>
                                  {m.role === "owner" && (
                                    <View style={styles.ownerBadge}>
                                      <Text style={styles.ownerBadgeText}>owner</Text>
                                    </View>
                                  )}
                                </View>
                                <Text style={styles.memberSkill}>
                                {(() => { try { return JSON.parse(m.skills).join(", "); } catch { return m.skills || ""; } })()}
                              </Text>
                              </View>
                            </View>
                          ))}
                        </View>
                      </ScrollView>
                    </View>
                  )}

                  <View style={styles.cardFooter}>
                    {pending > 0 && (
                      <View style={styles.pendingBadge}>
                        <Text style={styles.pendingBadgeText}>⏳ {pending} pending request{pending > 1 ? "s" : ""}</Text>
                      </View>
                    )}
                    <Text style={styles.openBtnText}>Open Group →</Text>
                  </View>
                </TouchableOpacity>
              );
            })
          )}
          <View style={{ height: 100 }} />
        </ScrollView>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f1a" },
  header: {
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  title: { fontSize: 24, fontWeight: "800", color: "#fff" },
  scroll: { flex: 1, paddingHorizontal: 16 },
  empty: { alignItems: "center", paddingTop: 80 },
  emptyIcon: { fontSize: 48, marginBottom: 12 },
  emptyTitle: { color: "#fff", fontSize: 20, fontWeight: "700", marginBottom: 6 },
  emptyText: { color: "#666", fontSize: 14 },
  card: {
    backgroundColor: "#1a1a2e",
    borderRadius: 16,
    padding: 16,
    marginBottom: 14,
    borderWidth: 1,
    borderColor: "#ffffff10",
  },
  cardTop: { flexDirection: "row", justifyContent: "space-between", alignItems: "center", marginBottom: 6 },
  groupName: { color: "#fff", fontSize: 18, fontWeight: "800", flex: 1, marginRight: 8 },
  stageBadge: {
    backgroundColor: "#7c3aed30",
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderWidth: 1,
    borderColor: "#7c3aed60",
  },
  stageText: { color: "#a855f7", fontSize: 12, fontWeight: "600" },
  ideaText: { color: "#aaa", fontSize: 14, marginBottom: 16, lineHeight: 20 },
  stageBar: { flexDirection: "row", justifyContent: "space-between", marginBottom: 16, position: "relative" },
  stageStep: { alignItems: "center", flex: 1, zIndex: 1 },
  stageDot: { width: 10, height: 10, borderRadius: 5, backgroundColor: "#333", marginBottom: 4 },
  stageDotActive: { backgroundColor: "#7c3aed" },
  stageLabel: { color: "#555", fontSize: 10 },
  stageLabelActive: { color: "#a855f7" },
  stageConnector: {
    position: "absolute",
    top: 4,
    left: "12%",
    right: "12%",
    height: 2,
    backgroundColor: "#333",
    zIndex: 0,
  },
  stageConnectorFill: { height: "100%", backgroundColor: "#7c3aed" },
  members: { marginBottom: 14 },
  membersLabel: { color: "#666", fontSize: 11, marginBottom: 8 },
  memberRow: { flexDirection: "row", gap: 10 },
  memberChip: {
    flexDirection: "row",
    alignItems: "center",
    backgroundColor: "#ffffff08",
    borderRadius: 10,
    padding: 8,
    gap: 8,
  },
  memberAvatar: {
    width: 30,
    height: 30,
    borderRadius: 15,
    backgroundColor: "#7c3aed",
    alignItems: "center",
    justifyContent: "center",
  },
  memberAvatarOwner: { backgroundColor: "#a855f7" },
  memberAvatarText: { color: "#fff", fontSize: 10, fontWeight: "700" },
  memberName: { color: "#fff", fontSize: 13, fontWeight: "600" },
  memberSkill: { color: "#888", fontSize: 11 },
  ownerBadge: { backgroundColor: "#7c3aed40", borderRadius: 4, paddingHorizontal: 5, paddingVertical: 1 },
  ownerBadgeText: { color: "#a855f7", fontSize: 9, fontWeight: "700" },
  cardFooter: { flexDirection: "row", justifyContent: "space-between", alignItems: "center" },
  pendingBadge: {
    backgroundColor: "#f59e0b20",
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 5,
    borderWidth: 1,
    borderColor: "#f59e0b50",
  },
  pendingBadgeText: { color: "#f59e0b", fontSize: 12, fontWeight: "600" },
  openBtnText: { color: "#a855f7", fontWeight: "700", fontSize: 14 },
});
