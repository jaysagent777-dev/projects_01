import React, { useState } from "react";
import { View, Text, ScrollView, TouchableOpacity, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";

const SKILLS = ["App Analyst", "Product", "Developer", "Designer", "Marketer", "Finance", "Legal", "Sales"];

export default function ProfileScreen() {
  const [selectedSkills, setSelectedSkills] = useState(["App Analyst", "Product"]);

  const toggleSkill = (skill: string) => {
    setSelectedSkills((prev) =>
      prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]
    );
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        <View style={styles.profileHeader}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>JB</Text>
          </View>
          <Text style={styles.name}>Jay B.</Text>
          <Text style={styles.location}>📍 United States · Vizag roots</Text>
          <View style={styles.statRow}>
            <View style={styles.stat}>
              <Text style={styles.statNum}>1</Text>
              <Text style={styles.statLabel}>Groups</Text>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.stat}>
              <Text style={styles.statNum}>3</Text>
              <Text style={styles.statLabel}>Ideas liked</Text>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.stat}>
              <Text style={styles.statNum}>2</Text>
              <Text style={styles.statLabel}>Connections</Text>
            </View>
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>My Skills</Text>
          <Text style={styles.sectionSub}>What do you bring to a team?</Text>
          <View style={styles.skillGrid}>
            {SKILLS.map((skill) => (
              <TouchableOpacity
                key={skill}
                onPress={() => toggleSkill(skill)}
                style={[styles.skillChip, selectedSkills.includes(skill) && styles.skillChipActive]}
              >
                <Text style={[styles.skillText, selectedSkills.includes(skill) && styles.skillTextActive]}>
                  {skill}
                </Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Availability</Text>
          <View style={styles.availRow}>
            {["Side project", "Part-time", "Full-time"].map((a) => (
              <TouchableOpacity key={a} style={[styles.availChip, a === "Side project" && styles.availChipActive]}>
                <Text style={[styles.availText, a === "Side project" && styles.availTextActive]}>{a}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Looking to</Text>
          <View style={styles.availRow}>
            {["Start an idea", "Join a team", "Both"].map((a) => (
              <TouchableOpacity key={a} style={[styles.availChip, a === "Both" && styles.availChipActive]}>
                <Text style={[styles.availText, a === "Both" && styles.availTextActive]}>{a}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        <TouchableOpacity style={styles.saveBtn}>
          <Text style={styles.saveBtnText}>Save Profile</Text>
        </TouchableOpacity>

        <View style={{ height: 100 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f1a" },
  profileHeader: { alignItems: "center", paddingTop: 30, paddingBottom: 24, paddingHorizontal: 20 },
  avatar: {
    width: 80,
    height: 80,
    borderRadius: 40,
    backgroundColor: "#7c3aed",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 12,
  },
  avatarText: { color: "#fff", fontSize: 26, fontWeight: "800" },
  name: { color: "#fff", fontSize: 22, fontWeight: "800", marginBottom: 4 },
  location: { color: "#888", fontSize: 13, marginBottom: 20 },
  statRow: { flexDirection: "row", alignItems: "center" },
  stat: { alignItems: "center", paddingHorizontal: 24 },
  statNum: { color: "#fff", fontSize: 22, fontWeight: "800" },
  statLabel: { color: "#666", fontSize: 12 },
  statDivider: { width: 1, height: 30, backgroundColor: "#ffffff15" },
  section: { paddingHorizontal: 20, marginBottom: 24 },
  sectionTitle: { color: "#fff", fontSize: 17, fontWeight: "700", marginBottom: 4 },
  sectionSub: { color: "#666", fontSize: 13, marginBottom: 12 },
  skillGrid: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  skillChip: {
    paddingHorizontal: 14,
    paddingVertical: 8,
    borderRadius: 10,
    backgroundColor: "#1a1a2e",
    borderWidth: 1,
    borderColor: "#ffffff15",
  },
  skillChipActive: { backgroundColor: "#7c3aed", borderColor: "#7c3aed" },
  skillText: { color: "#888", fontSize: 13 },
  skillTextActive: { color: "#fff", fontWeight: "600" },
  availRow: { flexDirection: "row", gap: 8 },
  availChip: {
    flex: 1,
    paddingVertical: 10,
    borderRadius: 10,
    backgroundColor: "#1a1a2e",
    borderWidth: 1,
    borderColor: "#ffffff15",
    alignItems: "center",
  },
  availChipActive: { backgroundColor: "#7c3aed30", borderColor: "#7c3aed" },
  availText: { color: "#888", fontSize: 13 },
  availTextActive: { color: "#a855f7", fontWeight: "600" },
  saveBtn: {
    backgroundColor: "#7c3aed",
    marginHorizontal: 20,
    paddingVertical: 14,
    borderRadius: 14,
    alignItems: "center",
  },
  saveBtnText: { color: "#fff", fontSize: 16, fontWeight: "700" },
});
