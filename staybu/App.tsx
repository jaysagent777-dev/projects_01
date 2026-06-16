import { NavigationContainer } from "@react-navigation/native";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import { StatusBar } from "expo-status-bar";
import { Text } from "react-native";
import { SafeAreaProvider } from "react-native-safe-area-context";

import FeedScreen from "./src/screens/FeedScreen";
import GroupsScreen from "./src/screens/GroupsScreen";
import ProfileScreen from "./src/screens/ProfileScreen";

const Tab = createBottomTabNavigator();

export default function App() {
  return (
    <SafeAreaProvider>
      <NavigationContainer>
        <StatusBar style="light" />
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
            component={FeedScreen}
            options={{ tabBarIcon: ({ color }) => <Text style={{ fontSize: 20, color }}>💡</Text> }}
          />
          <Tab.Screen
            name="Groups"
            component={GroupsScreen}
            options={{ tabBarIcon: ({ color }) => <Text style={{ fontSize: 20, color }}>👥</Text> }}
          />
          <Tab.Screen
            name="Profile"
            component={ProfileScreen}
            options={{ tabBarIcon: ({ color }) => <Text style={{ fontSize: 20, color }}>👤</Text> }}
          />
        </Tab.Navigator>
      </NavigationContainer>
    </SafeAreaProvider>
  );
}
