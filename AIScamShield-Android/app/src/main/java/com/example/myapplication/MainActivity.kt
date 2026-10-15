
package com.example.myapplication

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.unit.dp
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

class MainActivity : ComponentActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContent {
            MaterialTheme {
                ScamShieldScreen()
            }
        }
    }
}

@Composable
fun ScamShieldScreen() {
    var message by remember { mutableStateOf("") }
    var result by remember { mutableStateOf("") }
    var confidence by remember { mutableStateOf("") }
    var loading by remember { mutableStateOf(false) }
    var note by remember { mutableStateOf("") }

    val scope = rememberCoroutineScope()

    Surface(modifier = Modifier.fillMaxSize()) {
        Column(
            modifier = Modifier
                .fillMaxSize()
                .verticalScroll(rememberScrollState())
                .padding(24.dp),
            horizontalAlignment = Alignment.CenterHorizontally
        ) {
            Spacer(modifier = Modifier.height(24.dp))

            Text(
                text = "AIScamShield",
                style = MaterialTheme.typography.headlineLarge
            )

            Spacer(modifier = Modifier.height(8.dp))
            Text("AI-Powered Scam Message Detection")

            Spacer(modifier = Modifier.height(24.dp))

            OutlinedTextField(
                value = message,
                onValueChange = { message = it },
                label = { Text("Enter a message") },
                placeholder = { Text("Paste the message here...") },
                modifier = Modifier.fillMaxWidth(),
                minLines = 4
            )

            Spacer(modifier = Modifier.height(16.dp))

            Button(
                modifier = Modifier.fillMaxWidth(),
                enabled = !loading,
                onClick = {
                    if (message.isBlank()) {
                        result = "Please enter a message."
                        confidence = ""
                        note = ""
                    } else {
                        loading = true
                        result = ""
                        confidence = ""
                        note = ""

                        scope.launch {
                            try {
                                val data = withContext(Dispatchers.IO) {
                                    val url = URL(
                                        "http://127.0.0.1:8000/check-message"
                                    )
                                    val connection =
                                        url.openConnection() as HttpURLConnection

                                    try {
                                        connection.requestMethod = "POST"
                                        connection.connectTimeout = 10000
                                        connection.readTimeout = 10000
                                        connection.doOutput = true
                                        connection.setRequestProperty(
                                            "Content-Type",
                                            "application/json"
                                        )

                                        val body = JSONObject()
                                            .put("message", message.trim())
                                            .toString()

                                        connection.outputStream.use {
                                            it.write(body.toByteArray(Charsets.UTF_8))
                                        }

                                        val status = connection.responseCode
                                        val stream = if (status in 200..299) {
                                            connection.inputStream
                                        } else {
                                            connection.errorStream
                                        }

                                        val responseText =
                                            stream.bufferedReader().use {
                                                it.readText()
                                            }

                                        if (status !in 200..299) {
                                            throw Exception("Server error: $responseText")
                                        }

                                        JSONObject(responseText)
                                    } finally {
                                        connection.disconnect()
                                    }
                                }

                                result = data.optString(
                                    "category",
                                    "Unable to classify"
                                )
                                confidence = data.optString("confidence", "")
                                note = data.optString("note", "")

                            } catch (e: Exception) {
                                result = "Connection failed"
                                note = e.localizedMessage
                                    ?: "Check your API server and network."
                            } finally {
                                loading = false
                            }
                        }
                    }
                }
            ) {
                Text(if (loading) "Checking..." else "Check Now")
            }

            Spacer(modifier = Modifier.height(24.dp))

            if (result.isNotBlank()) {
                Card(modifier = Modifier.fillMaxWidth()) {
                    Column(modifier = Modifier.padding(20.dp)) {
                        Text(
                            "Detection Result",
                            style = MaterialTheme.typography.titleLarge
                        )
                        Spacer(modifier = Modifier.height(12.dp))
                        Text(
                            result,
                            style = MaterialTheme.typography.headlineSmall
                        )

                        if (confidence.isNotBlank()) {
                            Spacer(modifier = Modifier.height(8.dp))
                            Text("Model confidence: $confidence%")
                        }

                        if (note.isNotBlank()) {
                            Spacer(modifier = Modifier.height(8.dp))
                            Text(note)
                        }
                    }
                }
            }

            Spacer(modifier = Modifier.height(20.dp))
            Text(
                "Prototype predictions can be incorrect. Verify suspicious payment requests independently.",
                style = MaterialTheme.typography.bodySmall
            )
        }
    }
}
