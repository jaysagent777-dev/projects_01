import React, { useCallback, useEffect, useState } from "react";
import {
  View, Text, ScrollView, TouchableOpacity, StyleSheet,
  TextInput, ActivityIndicator, Alert, RefreshControl,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";

const SKILLS = ["App Analyst", "Product", "Developer", "Designer", "Marketer", "Finance", "Legal", "Sales"];
const AVAILABILITIES = ["Side project", "Part-time", "Full-time"];

type Profile = {
  id: number;
  name: string;
  email: string;
  skills: string[] | string; // server returns JSON-parsed array or raw JSON string
  availability: string;
  location: string;
  ideas_count?: number;
  groups_count?: number;
};

export default function ProfileScreen() {
  const { user, logout } = useAuth();
  const [profile, setProfile] = useState<Profile | null>(null);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [saving, setSaving] = useState(false);

  // Editable fields
  const [name, setName] = useState("");
  const [selectedSkills, setSelectedSkills] = useState<string[]>([]);
  const [availability, setAvailability] = useState("Side project");
  const [location, setLocation] = useState("");

  const fetchProfile = useCallback(async () => {
    try {
      const data = await api.getProfile();
      setProfile(data);
      setName(data.name || "");
      const skills = Array.isArray(data.skills)
        ? data.skills
        : (() => { try { return JSON.parse(data.skills); } catch { return []; } })();
      setSelectedSkills(skills);
      setAvailability(data.availability || "Side project");
      setLocation(data.location || "");
    } catch (e: any) {
      Alert.alert("Error", e.message);
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  }, []);

  useEffect(() => {
    fetchProfile();
  }, [fetchProfile]);

  const toggleSkill = (skill: string) => {
    setSelectedSkills((prev) =>
      prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]
    );
  };

  const handleSave = async () => {
    setSaving(true);
    try {
      await api.updateProfile({ name, skills: selectedSkills, availability, location });
      Alert.alert("Saved!", "Your profile has been updated.");
    } catch (e: any) {
      Alert.alert("Error", e.message);
    } finally {
      setSaving(false);
    }
  };

  const handleLogout = () => {
    Alert.alert("Log out", "Are you sure?", [
      { text: "Cancel", style: "cancel" },
      { text: "Log out", style: "destructive", onPress: logout },
    ]);
  };

  const getInitials = (n: string) =>
    n.split(" ").map((w) => w[0]).join("").toUpperCase().slice(0, 2);

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <ActivityIndicator color="#7c3aed" style={{ marginTop: 80 }} />
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={() => { setRefreshing(true); fetchProfile(); }} tintColor="#7c3aed" />
        }
      >
        {/* Header */}
        <View style={styles.profileHeader}>
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>{getInitials(name || user?.name || "?")}</Text>
          </View>
          <TextInput
            style={styles.nameInput}
            value={name}
            onChangeText={setName}
            placeholder="Your name"
            placeholderTextColor="#555"
          />
          <Text style={styles.email}>{profile?.email || user?.email}</Text>

          <View style={styles.statRow}>
            <View style={styles.stat}>
              <Text style={styles.statNum}>{profile?.ideas_count ?? 0}</Text>
              <Text style={styles.statLabel}>Ideas posted</Text>
            </View>
            <View style={styles.statDivider} />
            <View style={styles.stat}>
              <Text style={styles.statNum}>{profile?.groups_count ?? 0}</Text>
              <Text style={styles.statLabel}>Groups joined</Text>
            </View>
          </View>
        </View>

        {/* Location */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Location</Text>
          <TextInput
            style={styles.textInput}
            value={location}
            onChangeText={setLocation}
            placeholder="City, Country"
            placeholderTextColor="#555"
          />
        </View>

        {/* Skills */}
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

        {/* Availability */}
        <View style={styles.section}>
          <Text style={styles.sectionTitle}>Availability</Text>
          <View style={styles.availRow}>
            {AVAILABILITIES.map((a) => (
              <TouchableOpacity
                key={a}
                onPress={() => setAvailability(a)}
                style={[styles.availChip, availability === a && styles.availChipActive]}
              >
                <Text style={[styles.availText, availability === a && styles.availTextActive]}>{a}</Text>
              </TouchableOpacity>
            ))}
          </View>
        </View>

        {/* Save */}
        <TouchableOpacity style={styles.saveBtn} onPress={handleSave} disabled={saving}>
          {saving ? (
            <ActivityIndicator color="#fff" />
          ) : (
            <Text style={styles.saveBtnText}>Save Profile</Text>
          )}
        </TouchableOpacity>

        {/* Logout */}
        <TouchableOpacity style={styles.logoutBtn} onPress={handleLogout}>
          <Text style={styles.logoutBtnText}>Log Out</Text>
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
    width: 80, height: 80, borderRadius: 40, backgroundColor: "#7c3aed",
    alignItems: "center", justifyContent: "center", marginBottom: 12,
  },
  avatarText: { color: "#fff", fontSize: 26, fontWeight: "800" },
  nameInput: {
    color: "#fff", fontSize: 22, fontWeight: "800", marginBottom: 4,
    textAlign: "center", borderBottomWidth: 1, borderBottomColor: "#ffffff20",
    paddingBottom: 4, minWidth: 160,
  },
  email: { color: "#666", fontSize: 13, marginBottom: 20 },
  statRow: { flexDirection: "row", alignItems: "center" },
  stat: { alignItems: "center", paddingHorizontal: 28 },
  statNum: { color: "#fff", fontSize: 22, fontWeight: "800" },
  statLabel: { color: "#666", fontSize: 12 },
  statDivider: { width: 1, height: 30, backgroundColor: "#ffffff15" },
  section: { paddingHorizontal: 20, marginBottom: 24 },
  sectionTitle: { color: "#fff", fontSize: 17, fontWeight: "700", marginBottom: 4 },
  sectionSub: { color: "#666", fontSize: 13, marginBottom: 12 },
  textInput: {
    backgroundColor: "#1a1a2e", borderRadius: 10, padding: 12,
    color: "#fff", fontSize: 14, borderWidth: 1, borderColor: "#ffffff15",
  },
  skillGrid: { flexDirection: "row", flexWrap: "wrap", gap: 8 },
  skillChip: {
    paddingHorizontal: 14, paddingVertical: 8, borderRadius: 10,
    backgroundColor: "#1a1a2e", borderWidth: 1, borderColor: "#ffffff15",
  },
  skillChipActive: { backgroundColor: "#7c3aed", borderColor: "#7c3aed" },
  skillText: { color: "#888", fontSize: 13 },
  skillTextActive: { color: "#fff", fontWeight: "600" },
  availRow: { flexDirection: "row", gap: 8 },
  availChip: {
    flex: 1, paddingVertical: 10, borderRadius: 10,
    backgroundColor: "#1a1a2e", borderWidth: 1, borderColor: "#ffffff15", alignItems: "center",
  },
  availChipActive: { backgroundColor: "#7c3aed30", borderColor: "#7c3aed" },
  availText: { color: "#888", fontSize: 13 },
  availTextActive: { color: "#a855f7", fontWeight: "600" },
  saveBtn: {
    backgroundColor: "#7c3aed", marginHorizontal: 20, paddingVertical: 14,
    borderRadius: 14, alignItems: "center", marginBottom: 12,
  },
  saveBtnText: { color: "#fff", fontSize: 16, fontWeight: "700" },
  logoutBtn: {
    marginHorizontal: 20, paddingVertical: 14, borderRadius: 14,
    alignItems: "center", borderWidth: 1, borderColor: "#ff444440", backgroundColor: "#ff444410",
  },
  logoutBtnText: { color: "#ff6666", fontSize: 16, fontWeight: "700" },
});
