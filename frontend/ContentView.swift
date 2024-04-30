//
//  ContentView.swift
//  FrontendBookApp
//
//  Created by Naif Albasheer on 29/04/2024.
//



import SwiftUI

struct ContentView: View {
    @ObservedObject var viewModel = BookViewModel()

    var body: some View {
        NavigationView {
            List(viewModel.books) { book in
                NavigationLink(destination: BookDetailView(book: book)) {
                    HStack {
                        // Placeholder for book image/thumbnail
                        Image(systemName: "book")
                            .resizable()
                            .aspectRatio(contentMode: .fit)
                            .frame(width: 50, height: 50)
                            .background(Color.gray.opacity(0.3))
                            .cornerRadius(8)
                        
                        VStack(alignment: .leading) {
                            Text(book.title)
                                .font(.headline)
                                .foregroundColor(.primary)
                            Text(book.author)
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                        Spacer()
                    }
                    .padding(.vertical, 4)
                }
            }
            .onAppear {
                viewModel.fetchBooks()
            }
            .navigationTitle("Books")
            .listStyle(PlainListStyle())
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}
