import React, { useState } from "react";
import {
  View, Text, TextInput, TouchableOpacity,
  StyleSheet, KeyboardAvoidingView, Platform, Alert,
} from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useAuth } from "../context/AuthContext";

export default function AuthScreen() {
  const { login, register } = useAuth();
  const [mode, setMode] = useState<"login" | "register">("login");
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const submit = async () => {
    setLoading(true);
    try {
      if (mode === "login") {
        await login(email, password);
      } else {
        await register(name, email, password);
      }
    } catch (e: any) {
      Alert.alert("Error", e.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView behavior={Platform.OS === "ios" ? "padding" : undefined} style={styles.inner}>
        <View style={styles.header}>
          <Text style={styles.logo}>Styabu</Text>
          <Text style={styles.tagline}>Build together</Text>
        </View>

        <View style={styles.tabs}>
          {(["login", "register"] as const).map((m) => (
            <TouchableOpacity key={m} onPress={() => setMode(m)} style={[styles.tab, mode === m && styles.tabActive]}>
              <Text style={[styles.tabText, mode === m && styles.tabTextActive]}>
                {m === "login" ? "Sign In" : "Create Account"}
              </Text>
            </TouchableOpacity>
          ))}
        </View>

        <View style={styles.form}>
          {mode === "register" && (
            <TextInput
              style={styles.input}
              placeholder="Your name"
              placeholderTextColor="#555"
              value={name}
              onChangeText={setName}
              autoCapitalize="words"
            />
          )}
          <TextInput
            style={styles.input}
            placeholder="Email"
            placeholderTextColor="#555"
            value={email}
            onChangeText={setEmail}
            keyboardType="email-address"
            autoCapitalize="none"
          />
          <TextInput
            style={styles.input}
            placeholder="Password"
            placeholderTextColor="#555"
            value={password}
            onChangeText={setPassword}
            secureTextEntry
          />
          <TouchableOpacity style={styles.btn} onPress={submit} disabled={loading}>
            <Text style={styles.btnText}>{loading ? "..." : mode === "login" ? "Sign In" : "Create Account"}</Text>
          </TouchableOpacity>
        </View>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: "#0f0f1a" },
  inner: { flex: 1, justifyContent: "center", paddingHorizontal: 24 },
  header: { alignItems: "center", marginBottom: 40 },
  logo: { fontSize: 40, fontWeight: "900", color: "#fff", letterSpacing: -1 },
  tagline: { color: "#a855f7", fontSize: 15, marginTop: 4 },
  tabs: { flexDirection: "row", backgroundColor: "#1a1a2e", borderRadius: 12, padding: 4, marginBottom: 24 },
  tab: { flex: 1, paddingVertical: 10, alignItems: "center", borderRadius: 10 },
  tabActive: { backgroundColor: "#7c3aed" },
  tabText: { color: "#666", fontWeight: "600" },
  tabTextActive: { color: "#fff" },
  form: { gap: 12 },
  input: {
    backgroundColor: "#1a1a2e",
    borderRadius: 12,
    padding: 14,
    color: "#fff",
    fontSize: 15,
    borderWidth: 1,
    borderColor: "#ffffff10",
  },
  btn: {
    backgroundColor: "#7c3aed",
    borderRadius: 12,
    padding: 16,
    alignItems: "center",
    marginTop: 4,
  },
  btnText: { color: "#fff", fontWeight: "700", fontSize: 16 },
});
