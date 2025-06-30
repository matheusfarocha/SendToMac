//
//  ShareViewController.swift
//  SendToMacShare
//
//  Created by Matheus Rocha on 6/30/25.
//

import UIKit
import Social

class ShareViewController: SLComposeServiceViewController {
    override func viewDidLoad() {
        super.viewDidLoad()
        
        if let item = extensionContext?.inputItems.first as? NSExtensionItem,
           let attachments = item.attachments {
            for attachment in attachments {
                if attachment.hasItemConformingToTypeIdentifier("public.url") {
                    attachment.loadItem(forTypeIdentifier: "public.url", options: nil) { (data, error) in
                        if let url = data as? URL {
                            // Send this URL to Supabase here
                            print("Received URL: \(url)")
                        }
                    }
                } else if attachment.hasItemConformingToTypeIdentifier("public.plain-text") {
                    attachment.loadItem(forTypeIdentifier: "public.plain-text", options: nil) { (data, error) in
                        if let text = data as? String {
                            // Send this text to Supabase here
                            print("Received text: \(text)")
                        }
                    }
                }
            }
        }
    }
    override func isContentValid() -> Bool {
        // Do validation of contentText and/or NSExtensionContext attachments here
        return true
    }

    override func didSelectPost() {
        // This is called after the user selects Post. Do the upload of contentText and/or NSExtensionContext attachments.
    
        // Inform the host that we're done, so it un-blocks its UI. Note: Alternatively you could call super's -didSelectPost, which will similarly complete the extension context.
        self.extensionContext!.completeRequest(returningItems: [], completionHandler: nil)
    }

    override func configurationItems() -> [Any]! {
        // To add configuration options via table cells at the bottom of the sheet, return an array of SLComposeSheetConfigurationItem here.
        return []
    }

}
