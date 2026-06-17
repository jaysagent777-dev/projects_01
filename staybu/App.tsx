import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { StatusBar } from "expo-status-bar";
import { Text, View, ActivityIndicator } from "react-native";
import { SafeAreaProvider } from "react-native-safe-area-context";

import FeedScreen from "./src/screens/FeedScreen";
import GroupsScreen from "./src/screens/GroupsScreen";
import ProfileScreen from "./src/screens/ProfileScreen";
import AuthScreen from "./src/screens/AuthScreen";
import GroupDetailScreen from "./src/screens/GroupDetailScreen";
import IdeaDetailScreen from "./src/screens/IdeaDetailScreen";
import { AuthProvider, useAuth } from "./src/context/AuthContext";

const Tab = createBottomTabNavigator();
const FeedStack = createNativeStackNavigator();
const GroupsStack = createNativeStackNavigator();
const ProfileStack = createNativeStackNavigator();

function FeedStackNavigator() {
  return (
    <FeedStack.Navigator screenOptions={{ headerShown: false }}>
      <FeedStack.Screen name="FeedMain" component={FeedScreen} />
      <FeedStack.Screen name="IdeaDetail" component={IdeaDetailScreen} />
      <FeedStack.Screen name="GroupDetail" component={GroupDetailScreen} />
    </FeedStack.Navigator>
  );
}

function GroupsStackNavigator() {
  return (
    <GroupsStack.Navigator screenOptions={{ headerShown: false }}>
      <GroupsStack.Screen name="GroupsMain" component={GroupsScreen} />
      <GroupsStack.Screen name="GroupDetail" component={GroupDetailScreen} />
    </GroupsStack.Navigator>
  );
}

function ProfileStackNavigator() {
  return (
    <ProfileStack.Navigator screenOptions={{ headerShown: false }}>
      <ProfileStack.Screen name="ProfileMain" component={ProfileScreen} />
    </ProfileStack.Navigator>
  );
}

function AppNavigator() {
  const { user, loading } = useAuth();

  if (loading) {
    return (
      <View style={{ flex: 1, backgroundColor: "#0f0f1a", alignItems: "center", justifyContent: "center" }}>
        <ActivityIndicator color="#7c3aed" size="large" />
      </View>
    );
  }

  if (!user) return <AuthScreen />;

  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: "#0f0f1a",
          borderTopColor: "#ffffff10",
          paddingBottom: 8,
          paddingTop: 8,
          height: 64,
        },
        tabBarActiveTintColor: "#a855f7",
        tabBarInactiveTintColor: "#555",
        tabBarLabelStyle: { fontSize: 11, fontWeight: "600" },
      }}
    >
      <Tab.Screen
        name="Feed"
        component={FeedStackNavigator}
        options={{ tabBarIcon: ({ color }) => <Text style={{ fontSize: 20, color }}>💡</Text> }}
      />
      <Tab.Screen
        name="Groups"
        component={GroupsStackNavigator}
        options={{ tabBarIcon: ({ color }) => <Text style={{ fontSize: 20, color }}>👥</Text> }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileStackNavigator}
        options={{ tabBarIcon: ({ color }) => <Text style={{ fontSize: 20, color }}>👤</Text> }}
      />
    </Tab.Navigator>
  );
}

export default function App() {
  return (
    <SafeAreaProvider>
      <AuthProvider>
        <NavigationContainer>
          <StatusBar style="light" />
          <AppNavigator />
        </NavigationContainer>
      </AuthProvider>
    </SafeAreaProvider>
  );
}
