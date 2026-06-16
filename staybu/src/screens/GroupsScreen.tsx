import React from "react";
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { MY_GROUPS } from "../data/mock";

const STAGES = ["Idea", "Validating", "Building", "Launched"];

export default function GroupsScreen() {
  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Text style={styles.title}>My Groups</Text>
        <TouchableOpacity style={styles.newBtn}>
          <Text style={styles.newBtnText}>+ New Idea</Text>
        </TouchableOpacity>
      </View>

      <ScrollView style={styles.scroll} showsVerticalScrollIndicator={false}>
        {MY_GROUPS.length === 0 ? (
          <View style={styles.empty}>
            <Text style={styles.emptyIcon}>🚀</Text>
            <Text style={styles.emptyTitle}>No groups yet</Text>
            <Text style={styles.emptyText}>Post an idea or join one from the feed</Text>
          </View>
        ) : (
          MY_GROUPS.map((group) => (
            <View key={group.id} style={styles.card}>
              <View style={styles.cardTop}>
                <Text style={styles.groupName}>{group.name}</Text>
                <View style={styles.stageBadge}>
                  <Text style={styles.stageText}>{group.stage}</Text>
                </View>
              </View>
              <Text style={styles.ideaText}>{group.idea}</Text>

              <View style={styles.stageBar}>
                {STAGES.map((s, i) => (
                  <View key={s} style={styles.stageStep}>
                    <View
                      style={[
                        styles.stageDot,
                        STAGES.indexOf(group.stage) >= i && styles.stageDotActive,
                      ]}
                    />
                    <Text style={styles.stageLabel}>{s}</Text>
                  </View>
                ))}
              </View>

              <View style={styles.members}>
                <Text style={styles.membersLabel}>Team</Text>
                <View style={styles.memberRow}>
                  {group.members.map((m) => (
                    <View key={m.id} style={styles.memberChip}>
                      <View style={styles.memberAvatar}>
                        <Text style={styles.memberAvatarText}>{m.avatar}</Text>
                      </View>
                      <View>
                        <Text style={styles.memberName}>{m.name}</Text>
                        <Text style={styles.memberSkill}>{m.skill}</Text>
                      </View>
                    </View>
                  ))}
                </View>
              </View>

              <TouchableOpacity style={styles.openBtn}>
                <Text style={styles.openBtnText}>Open Group →</Text>
              </TouchableOpacity>
            </View>
          ))
        )}
        <View style={{ height: 100 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f1a" },
  header: {
    flexDirection: "row",
    justifyContent: "space-between",
    alignItems: "center",
    paddingHorizontal: 20,
    paddingVertical: 12,
  },
  title: { fontSize: 24, fontWeight: "800", color: "#fff" },
  newBtn: {
    backgroundColor: "#7c3aed",
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 10,
  },
  newBtnText: { color: "#fff", fontWeight: "700", fontSize: 13 },
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
  groupName: { color: "#fff", fontSize: 20, fontWeight: "800" },
  stageBadge: {
    backgroundColor: "#7c3aed30",
    borderRadius: 8,
    paddingHorizontal: 10,
    paddingVertical: 4,
    borderWidth: 1,
    borderColor: "#7c3aed60",
  },
  stageText: { color: "#a855f7", fontSize: 12, fontWeight: "600" },
  ideaText: { color: "#aaa", fontSize: 14, marginBottom: 16 },
  stageBar: { flexDirection: "row", justifyContent: "space-between", marginBottom: 16 },
  stageStep: { alignItems: "center", flex: 1 },
  stageDot: {
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: "#333",
    marginBottom: 4,
  },
  stageDotActive: { backgroundColor: "#7c3aed" },
  stageLabel: { color: "#666", fontSize: 10 },
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
  memberAvatarText: { color: "#fff", fontSize: 10, fontWeight: "700" },
  memberName: { color: "#fff", fontSize: 13, fontWeight: "600" },
  memberSkill: { color: "#888", fontSize: 11 },
  openBtn: {
    borderWidth: 1,
    borderColor: "#7c3aed",
    borderRadius: 10,
    paddingVertical: 10,
    alignItems: "center",
  },
  openBtnText: { color: "#a855f7", fontWeight: "700", fontSize: 14 },
});
