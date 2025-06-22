//
//  ContentView.swift
//  SendToMac
//
//  Created by Matheus Rocha on 6/19/25.
//

import SwiftUI

enum AlertType: Identifiable {
    case success, failure
    
    var id: Int {
        hashValue
    }
}

struct ContentView: View {
    @State private var selectedType: String = ""
    @State private var data: String = ""
    @State private var alertType: AlertType?
    
    func getSecret(_ key: String) -> String {
        guard let path = Bundle.main.path(forResource: "Secrets", ofType: "plist"),
              let dict = NSDictionary(contentsOfFile: path),
              let value = dict[key] as? String else {
            fatalError("Missing key \(key) in Secrets.plist")
        }
        return value
    }
    
    
    func sendToSupabase() {
        let supabaseURL = getSecret("SUPABASE_URL")
        let supabaseKey = getSecret("SUPABASE_KEY")
        guard let url = URL(string: "\(supabaseURL)/rest/v1/Main") else { return }

        
        var request = URLRequest(url: url)
        request.addValue("Bearer \(supabaseKey)", forHTTPHeaderField: "Authorization")
        request.addValue(supabaseKey, forHTTPHeaderField: "apikey")
        
        request.httpMethod = "POST"
        
        // Your Supabase API key
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")
        request.addValue("application/json", forHTTPHeaderField: "Accept")
        request.addValue("true", forHTTPHeaderField: "Prefer") // needed for return=representation

        let body: [String: Any] = [
            "file_data": data,
            "file_type": selectedType,
            "is_read": false
        ]
        guard !selectedType.isEmpty, !data.isEmpty else {
            print("Missing data or type")
            alertType = .failure
            return
        }
        request.httpBody = try? JSONSerialization.data(withJSONObject: body)
        
        URLSession.shared.dataTask(with: request) { data, response, error in
            if let error = error {
                print("Error:", error.localizedDescription)
                DispatchQueue.main.async {
                    alertType = .failure
                }
                return
            }

            if let httpResponse = response as? HTTPURLResponse {
                print("Status code:", httpResponse.statusCode)
                if httpResponse.statusCode == 201 {
                    DispatchQueue.main.async {
                        alertType = .success
                    }
                } else {
                    DispatchQueue.main.async {
                        alertType = .failure
                    }
                    print("Response body:", String(data: data ?? Data(), encoding: .utf8) ?? "No body")
                }
            }
        }.resume()
        
    }
    
    var body: some View {
        VStack(spacing: 20) {
            Text("Choose type").font(.title)
            HStack {
                Menu(selectedType.isEmpty ? "Type" : selectedType) {
                    Button("URL") { selectedType = "URL" }
                    Button("TEXT") { selectedType = "TEXT" }
                }
                TextField("Data to send", text: $data)
                    .textFieldStyle(RoundedBorderTextFieldStyle())
            }
            
            Button("Send to Mac") {
                sendToSupabase()
            }
            .padding()
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(8)
        }
        .padding()
        .alert(item: $alertType) { type in
            switch type {
            case .success:
                return Alert(title: Text("Success"), message: Text("Data sent successfully!"), dismissButton: .default(Text("OK")))
            case .failure:
                return Alert(title: Text("Failure"), message: Text("Data Failed to send."), dismissButton: .default(Text("OK")))
            }
        }
    }
}
#Preview {
    ContentView()
}
