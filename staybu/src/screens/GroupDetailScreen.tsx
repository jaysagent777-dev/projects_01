import React, { useCallback, useEffect, useState } from "react";
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet,
  ActivityIndicator, Alert, RefreshControl,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const STAGES = ["Idea", "Validating", "Building", "Launched"];

type Member = {
  id: number;
  name: string;
  skills: string; // JSON string or comma-separated from server
  role: string;
};

type JoinRequest = {
  id: number;
  user_id: number;
  name: string;      // from JOIN users u ON jr.user_id = u.id
  skills: string;    // JSON string
  message: string;
  status: string;
  created_at: string;
};

type Group = {
  id: number;
  idea_id: number;
  idea_title: string;
  idea_description: string;
  stage: string;
  members: Member[];
  owner_id?: number; // derived from members role
};

export default function GroupDetailScreen({ route, navigation }: any) {
  const { group: initialGroup } = route.params;
  const { user } = useAuth();

  const [group, setGroup] = useState<Group>(initialGroup);
  const [requests, setRequests] = useState<JoinRequest[]>([]);
  const [loading, setLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [updatingStage, setUpdatingStage] = useState(false);

  // owner_id may be passed explicitly or derived from members list
  const ownerMember = group.members?.find((m) => m.role === "owner");
  const ownerId = group.owner_id ?? ownerMember?.id;
  const isOwner = user?.id === ownerId;

  const fetchRequests = useCallback(async () => {
    if (!ownerId || user?.id !== ownerId) return;
    try {
      const reqs = await api.getJoinRequests(group.idea_id);
      setRequests(reqs.filter((r: JoinRequest) => r.status === "pending"));
    } catch {}
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ownerId, user?.id, group.idea_id]);

  const fetchGroup = useCallback(async () => {
    try {
      // Refresh from groups list
      const groups = await api.getMyGroups();
      const updated = groups.find((g: Group) => g.id === group.id);
      if (updated) setGroup(updated);
      await fetchRequests();
    } catch {} finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, [group.id, fetchRequests]);

  useEffect(() => {
    fetchRequests();
  }, [fetchRequests]);

  const handleStageChange = async (stage: string) => {
    if (!isOwner || stage === group.stage) return;
    setUpdatingStage(true);
    try {
      await api.updateStage(group.id, stage);
      setGroup((prev) => ({ ...prev, stage }));
    } catch (e: any) {
      Alert.alert("Error", e.message);
    } finally {
      setUpdatingStage(false);
    }
  };

  const handleApprove = async (requestId: number) => {
    try {
      await api.approveRequest(requestId);
      setRequests((prev) => prev.filter((r) => r.id !== requestId));
      Alert.alert("Approved!", "The member has been added to your group.");
      fetchGroup();
    } catch (e: any) {
      Alert.alert("Error", e.message);
    }
  };

  const handleReject = (requestId: number) => {
    // Optimistically remove — no reject endpoint, just remove from UI
    setRequests((prev) => prev.filter((r) => r.id !== requestId));
  };

  const handleLeave = () => {
    Alert.alert("Leave Group", "Are you sure you want to leave this group?", [
      { text: "Cancel", style: "cancel" },
      {
        text: "Leave", style: "destructive", onPress: () => {
          // Navigate back — actual leave functionality would need an API endpoint
          navigation.goBack();
        }
      },
    ]);
  };

  const getInitials = (name: string) =>
    name.split(" ").map((n) => n[0]).join("").toUpperCase().slice(0, 2);

  const stageIndex = STAGES.indexOf(group.stage);

  return (
    <SafeAreaView style={styles.container}>
      {/* Back button */}
      <View style={styles.topBar}>
        <TouchableOpacity onPress={() => navigation.goBack()} style={styles.backBtn}>
          <Text style={styles.backBtnText}>← Back</Text>
        </TouchableOpacity>
      </View>

      <ScrollView
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={() => { setRefreshing(true); fetchGroup(); }} tintColor="#7c3aed" />
        }
      >
        {/* Header */}
        <View style={styles.header}>
          <Text style={styles.title}>{group.idea_title}</Text>
          {group.idea_description ? (
            <Text style={styles.description}>{group.idea_description}</Text>
          ) : null}
        </View>

        {/* Stage selector */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Stage</Text>
            {updatingStage && <ActivityIndicator color="#7c3aed" size="small" />}
          </View>
          <View style={styles.stageGrid}>
            {STAGES.map((s, i) => (
              <TouchableOpacity
                key={s}
                style={[
                  styles.stageChip,
                  stageIndex >= i && styles.stageChipActive,
                  group.stage === s && styles.stageChipCurrent,
                  !isOwner && styles.stageChipDisabled,
                ]}
                onPress={() => handleStageChange(s)}
                disabled={!isOwner || updatingStage}
              >
                <Text style={[
                  styles.stageChipText,
                  stageIndex >= i && styles.stageChipTextActive,
                  group.stage === s && styles.stageChipTextCurrent,
                ]}>
                  {s}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
          {!isOwner && <Text style={styles.ownerNote}>Only the owner can change the stage</Text>}
        </View>

        {/* Members */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Team ({group.members?.length || 0})</Text>
          {group.members && group.members.length > 0 ? (
            group.members.map((m) => (
              <View key={m.id} style={styles.memberRow}>
                <View style={[styles.memberAvatar, m.role === "owner" && styles.memberAvatarOwner]}>
                  <Text style={styles.memberAvatarText}>{getInitials(m.name)}</Text>
                </View>
                <View style={{ flex: 1 }}>
                  <Text style={styles.memberName}>{m.name}</Text>
                  <Text style={styles.memberSkill}>
                    {(() => { try { return JSON.parse(m.skills).join(", "); } catch { return m.skills || ""; } })()}
                  </Text>
                </View>
                {m.role === "owner" && (
                  <View style={styles.ownerBadge}>
                    <Text style={styles.ownerBadgeText}>owner</Text>
                  </View>
                )}
              </View>
            ))
          ) : (
            <Text style={styles.emptyText}>No members yet</Text>
          )}
        </View>

        {/* Pending requests (owner only) */}
        {isOwner && (
          <View style={styles.section}>
            <Text style={styles.sectionTitle}>Pending Requests ({requests.length})</Text>
            {requests.length === 0 ? (
              <View style={styles.emptyRequests}>
                <Text style={styles.emptyText}>No pending requests</Text>
              </View>
            ) : (
              requests.map((req) => (
                <View key={req.id} style={styles.requestCard}>
                  <View style={styles.requestHeader}>
                    <View style={styles.memberAvatar}>
                      <Text style={styles.memberAvatarText}>{getInitials(req.name)}</Text>
                    </View>
                    <View style={{ flex: 1 }}>
                      <Text style={styles.memberName}>{req.name}</Text>
                      {req.skills ? (
                        <Text style={styles.memberSkill}>
                          {(() => { try { return JSON.parse(req.skills).join(", "); } catch { return req.skills; } })()}
                        </Text>
                      ) : null}
                    </View>
                  </View>
                  {req.message ? (
                    <Text style={styles.requestMessage}>"{req.message}"</Text>
                  ) : null}
                  <View style={styles.requestActions}>
                    <TouchableOpacity style={styles.approveBtn} onPress={() => handleApprove(req.id)}>
                      <Text style={styles.approveBtnText}>✓ Approve</Text>
                    </TouchableOpacity>
                    <TouchableOpacity style={styles.rejectBtn} onPress={() => handleReject(req.id)}>
                      <Text style={styles.rejectBtnText}>✕ Reject</Text>
                    </TouchableOpacity>
                  </View>
                </View>
              ))
            )}
          </View>
        )}

        {/* Leave button for non-owners */}
        {!isOwner && (
          <TouchableOpacity style={styles.leaveBtn} onPress={handleLeave}>
            <Text style={styles.leaveBtnText}>Leave Group</Text>
          </TouchableOpacity>
        )}

        <View style={{ height: 100 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f1a" },
  topBar: { paddingHorizontal: 16, paddingVertical: 8 },
  backBtn: { padding: 4 },
  backBtnText: { color: "#a855f7", fontSize: 16, fontWeight: "600" },
  header: { paddingHorizontal: 20, paddingTop: 8, paddingBottom: 20 },
  title: { color: "#fff", fontSize: 24, fontWeight: "800", marginBottom: 8 },
  description: { color: "#aaa", fontSize: 15, lineHeight: 22 },
  section: { paddingHorizontal: 20, marginBottom: 28 },
  sectionHeader: { flexDirection: "row", alignItems: "center", justifyContent: "space-between", marginBottom: 12 },
  sectionTitle: { color: "#fff", fontSize: 17, fontWeight: "700", marginBottom: 12 },
  ownerNote: { color: "#555", fontSize: 12, marginTop: 8 },
  stageGrid: { flexDirection: "row", gap: 8, flexWrap: "wrap" },
  stageChip: {
    flex: 1, paddingVertical: 10, borderRadius: 10, backgroundColor: "#1a1a2e",
    borderWidth: 1, borderColor: "#ffffff15", alignItems: "center", minWidth: 70,
  },
  stageChipActive: { backgroundColor: "#7c3aed20", borderColor: "#7c3aed50" },
  stageChipCurrent: { backgroundColor: "#7c3aed", borderColor: "#7c3aed" },
  stageChipDisabled: { opacity: 0.7 },
  stageChipText: { color: "#666", fontSize: 13, fontWeight: "600" },
  stageChipTextActive: { color: "#a855f7" },
  stageChipTextCurrent: { color: "#fff" },
  memberRow: {
    flexDirection: "row", alignItems: "center", backgroundColor: "#1a1a2e",
    borderRadius: 12, padding: 12, marginBottom: 8, borderWidth: 1, borderColor: "#ffffff10",
  },
  memberAvatar: {
    width: 36, height: 36, borderRadius: 18, backgroundColor: "#7c3aed",
    alignItems: "center", justifyContent: "center", marginRight: 12,
  },
  memberAvatarOwner: { backgroundColor: "#a855f7" },
  memberAvatarText: { color: "#fff", fontSize: 11, fontWeight: "700" },
  memberName: { color: "#fff", fontSize: 14, fontWeight: "600" },
  memberSkill: { color: "#888", fontSize: 12 },
  ownerBadge: { backgroundColor: "#7c3aed40", borderRadius: 6, paddingHorizontal: 8, paddingVertical: 3 },
  ownerBadgeText: { color: "#a855f7", fontSize: 11, fontWeight: "700" },
  emptyRequests: { backgroundColor: "#1a1a2e", borderRadius: 12, padding: 20, alignItems: "center", borderWidth: 1, borderColor: "#ffffff10" },
  emptyText: { color: "#555", fontSize: 14 },
  requestCard: {
    backgroundColor: "#1a1a2e", borderRadius: 12, padding: 14,
    marginBottom: 10, borderWidth: 1, borderColor: "#ffffff10",
  },
  requestHeader: { flexDirection: "row", alignItems: "center", marginBottom: 8 },
  requestMessage: { color: "#aaa", fontSize: 13, fontStyle: "italic", marginBottom: 12, lineHeight: 18 },
  requestActions: { flexDirection: "row", gap: 8 },
  approveBtn: { flex: 1, backgroundColor: "#7c3aed", borderRadius: 8, paddingVertical: 8, alignItems: "center" },
  approveBtnText: { color: "#fff", fontWeight: "700", fontSize: 13 },
  rejectBtn: { flex: 1, backgroundColor: "#ff444420", borderRadius: 8, paddingVertical: 8, alignItems: "center", borderWidth: 1, borderColor: "#ff444440" },
  rejectBtnText: { color: "#ff6666", fontWeight: "700", fontSize: 13 },
  leaveBtn: {
    marginHorizontal: 20, paddingVertical: 14, borderRadius: 14,
    alignItems: "center", borderWidth: 1, borderColor: "#ff444440", backgroundColor: "#ff444410", marginBottom: 16,
  },
  leaveBtnText: { color: "#ff6666", fontSize: 16, fontWeight: "700" },
});
